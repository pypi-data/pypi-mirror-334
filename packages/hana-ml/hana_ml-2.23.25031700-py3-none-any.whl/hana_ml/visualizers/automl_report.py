"""
This module contains related class for generating the best pipeline report.

The following class is available:

    * :class:`BestPipelineReport`
"""

# pylint: disable=missing-module-docstring
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-function-args
# pylint: disable=too-many-instance-attributes
# pylint: disable=trailing-whitespace
# pylint: disable=protected-access
# pylint: disable=no-self-use
# pylint: disable=invalid-name
import json
from typing import List
import pandas as pd
from hana_ml import dataframe
from hana_ml.visualizers.digraph import MultiDigraph
from hana_ml.visualizers.report_builder import ReportBuilder, Page, TableItem, ChartItem, DigraphItem, ConnectionsItem
from hana_ml.visualizers.shared import EmbeddedUI


class _PipelineWalk:  # from hana_ml.algorithms.pal.auto_ml import _PipelineWalk
    def __init__(self, pipeline):
        self.current_walk = pipeline
        self.end = False
        if isinstance(self.current_walk, dict):
            self.current_content = list(self.current_walk.keys())[0]
            self.current_args = list(self.current_walk.values())[0]['args']
        else:
            self.current_content = self.current_walk
            self.current_args = ''
            self.end = True

    def _next(self):
        if 'inputs' in self.current_walk[self.current_content]:
            if 'data' in self.current_walk[self.current_content]['inputs']:
                self.current_walk = self.current_walk[self.current_content]['inputs']['data']
                if isinstance(self.current_walk, dict):
                    self.current_content = list(self.current_walk.keys())[0]
                    self.current_args = list(self.current_walk.values())[0]['args']
                else:
                    self.current_content = self.current_walk
                    self.current_args = ''
                    self.end = True


class BestPipelineReport(object):
    """
    The instance of this class can generate the best pipeline report.

    Parameters
    ----------
    automatic_obj : :class:`~hana_ml.algorithms.pal.auto_ml.AutomaticClassification` or :class:`~hana_ml.algorithms.pal.auto_ml.AutomaticRegression` or :class:`~hana_ml.algorithms.pal.auto_ml.AutomaticTimeSeries`
        An instance of the AutomaticClassification / AutomaticRegression / AutomaticTimeSeries Class.

    Examples
    --------

    Create an AutomaticClassification instance:

    >>> progress_id = "automl_{}".format(uuid.uuid1())
    >>> auto_c = AutomaticClassification(generations=2,
                                         population_size=5,
                                         offspring_size=5,
                                         progress_indicator_id=progress_id)

    Training:

    >>> auto_c.fit(data=df_train)

    Plot the best pipeline:

    >>> BestPipelineReport(auto_c).generate_notebook_iframe()

    .. image:: image/best_pipeline_classification.png

    """
    def __init__(self, automatic_obj):
        best_pipeline_df: dataframe.DataFrame = None
        if hasattr(automatic_obj, "best_pipeline_"):
            best_pipeline_df = automatic_obj.best_pipeline_
        else:
            best_pipeline_df = automatic_obj.model_[1]

        highlighted_metric = automatic_obj._get_highlight_metric()

        connections_json_str = None
        for key_value in automatic_obj.info_.collect().to_dict('records'):
            if key_value['STAT_NAME'] == 'optimal_connections':
                connections_json_str = key_value['STAT_VALUE']
                break

        self.automatic_obj = automatic_obj
        self.report_builder: ReportBuilder = BestPipelineReport.create_report_builder(best_pipeline_df.collect(), highlighted_metric, connections_json_str)

    @staticmethod
    def create_report_builder(best_pipeline_pd_df: pd.DataFrame, highlighted_metric, connections_json_str=None):
        ids = list(best_pipeline_pd_df['ID'].astype(str))
        pipelines = list(best_pipeline_pd_df['PIPELINE'])
        scores = list(best_pipeline_pd_df['SCORES'])

        all_metric_values = []
        metric_values_dict = {}  # metric1 -> [v1,v2,...], metric2 -> [v1,v2,...]
        for metric_json_str in scores:
            metric_dict = json.loads(metric_json_str)
            for k in metric_dict:
                if metric_values_dict.get(k) is None:
                    metric_values_dict[k] = []
                metric_values_dict[k].append(metric_dict[k])
                all_metric_values.append(metric_dict[k])

        report_builder = ReportBuilder('Best Pipeline Report')

        page = Page('Overview')
        item = TableItem('Pipelines')
        item.addColumn('ID', ids)
        item.addColumn('PIPELINE', pipelines)
        page.addItem(item)

        item = TableItem('Metrics')
        item.addColumn('ID', ids)
        for metric in metric_values_dict:
            item.addColumn(metric, metric_values_dict[metric])
        page.addItem(item)
        report_builder.addPage(page)

        page = Page('Metrics')
        items = []
        min_max_dict = {}
        x_y_list = []
        for metric in metric_values_dict:
            metric_values = metric_values_dict[metric]
            mean = sum(metric_values) / len(metric_values)
            sum_mean = 0
            for d in metric_values:
                sum_mean = sum_mean + abs(float(d) - mean)
            mean = sum_mean / len(metric_values) + 0.1
            min_max_dict[metric] = [min(metric_values) - mean, max(metric_values) + mean]
            if metric != highlighted_metric:
                x_y_list.append([metric, highlighted_metric])

        metric_names = list(metric_values_dict.keys())
        parallelAxis = []
        series = []
        all_data = []
        for i in range(0, len(metric_names)):
            parallelAxis.append({
                'dim': i,
                'name': metric_names[i],
                'areaSelectStyle': 0
            })
        for i in range(0, len(ids)):
            data = []
            for metric in metric_names:
                data.append(metric_values_dict[metric][i])
            all_data.append(data)
            series.append({
                'name': "ID: " + ids[i],
                'type': 'parallel',
                'lineStyle': {
                    'width': 5
                },
                'emphasis': {
                    'focus': 'self'
                },
                'data': [data]
            })
        series.insert(0, {
            'name': '-',
            'type': 'parallel',
            'lineStyle': {
                'opacity': 0
            },
            'data': all_data
        })
        option = {
            'legend': {
                'type': 'scroll',
                'bottom': 0,
                'data': list(map(lambda id: "ID: " + id, ids))
            },
            'tooltip': {},
            'parallel': {
                'parallelAxisDefault': {
                    'nameLocation': 'middle',
                    'nameGap': -15
                }
            },
            'parallelAxis': parallelAxis,
            'series': series
        }
        if len(parallelAxis) > 15:
            item = ChartItem('Metric: Parallel Coordinates', option, width=len(parallelAxis) * 80)
        else:
            item = ChartItem('Metric: Parallel Coordinates', option)
        items.append(item)

        option = {
            'customFn': ['xAxis.axisLabel.formatter'],
            'grid': {
                'show': 1,
                'containLabel': 1
            },
            'legend': {},
            'xAxis': {
                'type': 'value',
                'name': highlighted_metric,
                'nameLocation': 'middle',
                'nameGap': 35,
                'boundaryGap': 1,
                'min': min_max_dict[highlighted_metric][0],
                'max': min_max_dict[highlighted_metric][1],
                'axisTick': {
                    'alignWithLabel': 1,
                    'show': 0
                },
                'axisLabel': {
                    'showMinLabel': 1,
                    'showMaxLabel': 1,
                    'hideOverlap': 1,
                    'rotate': 90,
                    'fontSize': 9,
                    'formatter': {
                        'params': ['val'],
                        'body': 'return parseFloat(val.toString().substring(0,6));'
                    }
                }
            },
            'yAxis': {
                'type': 'category',
                'name': 'ID',
                'data': ids,
                'axisLine': {
                    'show': 1,
                },
                'axisTick': {
                    'show': 1
                },
                'axisLabel': {
                    'showMinLabel': 1,
                    'showMaxLabel': 1,
                    'hideOverlap': 1,
                    'fontSize': 9,
                }
            },
            'tooltip': {
                'trigger': 'axis',
                'axisPointer': {
                    'type': 'shadow'
                }
            },
            'dataZoom': [
                {
                    'type': 'slider',
                    'show': 1,
                    'xAxisIndex': [0]
                },
                {
                    'type': 'inside',
                    'xAxisIndex': [0]
                }
            ],
            'series': [
                {
                    'type': 'bar',
                    'colorBy': 'data',
                    'data': metric_values_dict[highlighted_metric],
                    'symbol': 'none',
                    'smooth': 1,
                    'emphasis': {
                        'focus': 'series'
                    }
                }
            ]
        }
        items.append(ChartItem('Metric: {}-{}'.format(highlighted_metric, 'ID'), option, height=len(ids) * 30))

        for x_y in x_y_list:
            option_series = []
            index = 0
            for x in metric_values_dict[x_y[0]]:
                y = metric_values_dict[x_y[1]][index]
                z = ids[index]
                index = index + 1
                option_series.append({
                    'name': z,
                    'data': [[x, y, z]],
                    'emphasis': {
                        'focus': 'self'
                    },
                    'symbolSize': 25,
                    'type': 'scatter'
                })
            option = {
                'customFn': ['xAxis.axisLabel.formatter', 'yAxis.axisLabel.formatter'],
                'grid': {
                    'show': 1,
                    'containLabel': 1
                },
                'legend': {
                    'type': 'scroll',
                    'orient': 'vertical',
                    'right': 10,
                    'top': 20,
                    'bottom': 20,
                    'data': ids
                },
                'xAxis': {
                    'type': 'value',
                    'name': x_y[0],
                    'nameLocation': 'middle',
                    'nameGap': 35,
                    'boundaryGap': 1,
                    'min': min_max_dict[x_y[0]][0],
                    'max': min_max_dict[x_y[0]][1],
                    'axisTick': {
                        'alignWithLabel': 1,
                        'show': 0
                    },
                    'axisLabel': {
                        'showMinLabel': 1,
                        'showMaxLabel': 1,
                        'hideOverlap': 1,
                        'rotate': 90,
                        'fontSize': 9,
                        'formatter': {
                            'params': ['val'],
                            'body': 'return parseFloat(val.toString().substring(0,6));'
                        }
                    }
                },
                'yAxis': {
                    'type': 'value',
                    'name': x_y[1],
                    'min': min_max_dict[x_y[1]][0],
                    'max': min_max_dict[x_y[1]][1],
                    'axisLine': {
                        'show': 1,
                    },
                    'axisTick': {
                        'show': 1
                    },
                    'axisLabel': {
                        'showMinLabel': 1,
                        'showMaxLabel': 1,
                        'hideOverlap': 1,
                        'fontSize': 9,
                        'formatter': {
                            'params': ['val'],
                            'body': 'return parseFloat(val.toString().substring(0,6));'
                        }
                    }
                },
                'tooltip': {},
                'dataZoom': [
                    {
                        'type': 'slider',
                        'show': 1,
                        'xAxisIndex': [0]
                    },
                    {
                        'type': 'inside',
                        'xAxisIndex': [0]
                    }
                ],
                'series': option_series
            }
            if x_y[0] == 'LAYERS':
                option['xAxis']['inverse'] = 1
            items.append(ChartItem('Metric: {}-{}'.format(x_y[0], x_y[1]), option))
        page.addItems(items)
        report_builder.addPage(page)

        page = Page('Pipelines')
        def convert_to_digraph(pipelines: List[str]) -> MultiDigraph:
            multi_digraph: MultiDigraph = MultiDigraph('Pipelines', embedded_mode=True)
            for index in range(0, len(pipelines)):
                p_content = []
                p_args = []
                pipe = _PipelineWalk(json.loads(pipelines[index]))
                for i in range(1, 100):
                    p_content.append(pipe.current_content)
                    p_args.append(pipe.current_args)
                    pipe._next()
                    if pipe.end:
                        p_content.append(pipe.current_content)
                        p_args.append(pipe.current_args)
                        break
                p_content.reverse()
                p_args.reverse()
                count = 0
                nodes = []
                for p_1, p_2 in zip(p_content, p_args):
                    nodes.append((str(p_1), str(p_2), [str(count)], [str(count + 1)]))
                    count = count + 1
                digraph = multi_digraph.add_child_digraph('pipeline_{}'.format(index))
                node = []
                for elem in nodes:
                    node.append(digraph.add_python_node(elem[0],
                                                        elem[1],
                                                        in_ports=elem[2],
                                                        out_ports=elem[3]))
                for node_x in range(0, len(node) - 1):
                    digraph.add_edge(node[node_x].out_ports[0], node[node_x + 1].in_ports[0])
            multi_digraph.build()
            return multi_digraph
        item = DigraphItem('Pipelines', convert_to_digraph(pipelines))
        page.addItem(item)
        report_builder.addPage(page)

        if connections_json_str:
            page = Page('Connections')
            item = ConnectionsItem('Connections', connections_json_str)
            page.addItem(item)
            report_builder.addPage(page)

        return report_builder

    def generate_notebook_iframe(self, iframe_height: int = 1000):
        """
        Renders the best pipeline report as a notebook iframe.

        Parameters
        ----------
        iframe_height : int, optional
            Frame height.

            Defaults to 1000.
        """
        self.report_builder.generate_notebook_iframe(iframe_height)
        self.automatic_obj.report = EmbeddedUI.get_iframe_str(self.report_builder.html_str, iframe_height=iframe_height)

    def generate_html(self, filename: str):
        """
        Saves the best pipeline report as a html file.

        Parameters
        ----------
        filename : str
            Html file name.
        """
        self.report_builder.generate_html("{}_best_pipeline_report.html".format(filename))
