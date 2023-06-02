from figures import ModelPerformanceMetricsFigure


def generate_model_performance_metrics_figure(config, model_accuracy_and_loss_of_each_epoch, model_performance_metrics):
    figure = ModelPerformanceMetricsFigure(config)
    figure.add_traces(model_accuracy_and_loss_of_each_epoch, model_performance_metrics)
    figure.update_layout()
    figure.update_annotations()
    figure.write()
