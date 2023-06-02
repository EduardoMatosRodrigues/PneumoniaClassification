from figures import ModelPerformanceMetricsFigure, PatientFigure


def generate_patient_figure(config, model_prediction_result):
    figure = PatientFigure(config)
    figure.set_traces(
        model_prediction_result['cam_image'],
        model_prediction_result['original_image'][0], model_prediction_result['pneumonia_probability'])
    figure.set_shapes(model_prediction_result['patient_training_features'])
    figure.update_layout()
    figure.update_annotations()
    figure.write(model_prediction_result['patient_id'])


def generate_model_performance_metrics_figure(config, model_accuracy_and_loss_of_each_epoch, model_performance_metrics):
    figure = ModelPerformanceMetricsFigure(config)
    figure.add_traces(model_accuracy_and_loss_of_each_epoch, model_performance_metrics)
    figure.update_layout()
    figure.update_annotations()
    figure.write()
