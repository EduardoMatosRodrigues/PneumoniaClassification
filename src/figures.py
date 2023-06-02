import plotly.express as px
import plotly.graph_objects as go
import warnings
from plotly.subplots import make_subplots
warnings.filterwarnings("ignore")


class PatientFigure:

    def __init__(self, config):
        self._config = config
        self._figure = self.get_initial()

    @staticmethod
    def get_initial():
        return make_subplots(
            rows=1, cols=3, horizontal_spacing=0.075, subplot_titles=(
                "Chest x-ray with <br>pneumonia evidence bounding box",
                "Chest x-ray with <br>class activation map"))

    def set_shapes(self, training_features, resized_image_height=224, original_image_height=1024):
        resize_factor = resized_image_height / original_image_height
        rectangle_coordinates = dict(
            x0=training_features["x"] * resize_factor, y0=training_features["y"] * resize_factor,
            x1=training_features["x"] * resize_factor + training_features["width"] * resize_factor,
            y1=training_features["x"] * resize_factor + training_features["height"] * resize_factor)
        self._figure.add_shape(
            type="rect", x0=rectangle_coordinates['x0'], y0=rectangle_coordinates['y0'], x1=rectangle_coordinates['x1'],
            y1=rectangle_coordinates['y1'], line=dict(color="red"), row=1, col=1)

    def set_traces(self, cam_image, original_image, pneumonia_probability):
        self._figure.add_trace(px.imshow(original_image, binary_string=True).data[0], row=1, col=1)
        self._figure.add_trace(px.imshow(original_image, binary_string=True).data[0], row=1, col=2)
        self._figure.add_trace(go.Heatmap(z=cam_image, colorscale='jet', opacity=0.3, showscale=False), row=1, col=2)
        self._figure.add_trace(go.Indicator(
            domain=dict(x=[0.72, 0.9], y=[0, 1]), number=dict(suffix="%", font=dict(size=15)), mode="gauge+number",
            value=pneumonia_probability, title=dict(text="Pneumonia probability", font=dict(size=12)),
            gauge=dict(
                axis=dict(dtick=25, range=[None, 100]),
                steps=[dict(range=[50, 75], color="orange"), dict(range=[75, 100], color="red")])))

    def update_annotations(self):
        self._figure.update_annotations(font_size=12, yshift=-30)

    def update_layout(self):
        self._figure.update_layout(
            height=500, margin=dict(l=50, r=0), title=dict(
                text="Pneumonia probability on chest x-rays", font=dict(size=22),
                x=0.5, y=0.9, xanchor='center', yanchor='top'),
            width=800)

    def write(self, patient_id):
        self._figure.write_image(
            f"{self._config.model.prediction_results.dir}/{patient_id}.png")


class ModelPerformanceMetricsFigure:

    def __init__(self, config):
        self._config = config
        self._figure = self.get_initial()

    @staticmethod
    def get_initial():
        return make_subplots(
            rows=2, cols=2, specs=[[{}, {}], [{"colspan": 2}, None]], horizontal_spacing=0.2, vertical_spacing=0.35,
            subplot_titles=("Confusion matrix", "Accuracy and loss of each epoch", "General performance metrics"))

    def add_traces(self, model_accuracy_and_loss_of_each_epoch, model_performance_metrics):
        self._figure.add_trace(go.Scatter(
            x=model_accuracy_and_loss_of_each_epoch.index, y=model_accuracy_and_loss_of_each_epoch['Train accuracy'],
            mode='lines', name='Train accuracy', line=dict(color='green')), row=1, col=2)
        self._figure.add_trace(go.Scatter(
            x=model_accuracy_and_loss_of_each_epoch.index, y=model_accuracy_and_loss_of_each_epoch['Train loss'],
            mode='lines', name='Train loss', line=dict(color='red')), row=1, col=2)
        self._figure.add_trace(go.Scatter(
            x=model_accuracy_and_loss_of_each_epoch.index, y=model_accuracy_and_loss_of_each_epoch['Validation accuracy'],
            mode='lines', name='Validation accuracy', line=dict(color='green', dash='dash')), row=1, col=2)
        self._figure.add_trace(go.Scatter(
            x=model_accuracy_and_loss_of_each_epoch.index, y=model_accuracy_and_loss_of_each_epoch['Validation loss'],
            mode='lines', name='Validation loss', line=dict(color='red', dash='dash')), row=1, col=2)
        self._figure.add_trace(go.Heatmap(
            z=[[0.5, 0], [0, 0.5]], x=['No', 'Yes'], y=['No', 'Yes'], hoverinfo='skip', colorscale='Oranges', showscale=False,
            text=model_performance_metrics['confusion_matrix'].numpy().astype(int).astype(str).tolist(),
            texttemplate="<b>%{text}<b>", textfont={"size": 20}, zmin=0, zmax=1), row=1, col=1)
        self._figure.add_trace(go.Indicator(
            domain=dict(x=[0.01, 0.27], y=[0, 0.2]), number=dict(suffix="%", font=dict(size=15)), mode="gauge+number",
            value=round(100 * float(model_performance_metrics['accuracy']), 2),
            title=dict(text="Accuracy", font=dict(size=14)),
            gauge=dict(
                axis=dict(dtick=25, range=[None, 100]),
                steps=[dict(range=[50, 75], color="orange"), dict(range=[75, 100], color="red")])))
        self._figure.add_trace(go.Indicator(
            domain=dict(x=[0.37, 0.63], y=[0, 0.2]), number=dict(suffix="%", font=dict(size=15)), mode="gauge+number",
            value=round(100 * float(model_performance_metrics['precision']), 2),
            title=dict(text="Precision", font=dict(size=14)),
            gauge=dict(
                axis=dict(dtick=25, range=[None, 100]),
                steps=[dict(range=[50, 75], color="orange"), dict(range=[75, 100], color="red")])))
        self._figure.add_trace(go.Indicator(
            domain=dict(x=[0.73, 0.99], y=[0, 0.2]), number=dict(suffix="%", font=dict(size=15)), mode="gauge+number",
            value=round(100 * float(model_performance_metrics['recall']), 2),
            title=dict(text="Recall", font=dict(size=14)),
            gauge=dict(
                axis=dict(dtick=25, range=[None, 100]),
                steps=[dict(range=[50, 75], color="orange"), dict(range=[75, 100], color="red")])))

    def update_annotations(self):
        self._figure.update_annotations(font_size=16, yshift=20)

    def update_layout(self):
        self._figure.update_layout(
            title=dict(
                text="Model training performance metrics",
                font=dict(size=22), x=0.5, y=0.9, xanchor='center', yanchor='top'),
            margin=dict(l=150, r=150, b=50, t=150),
            xaxis2=dict(title=dict(text="Epochs", font=dict(size=12))),
            yaxis2=dict(range=[0, 1.001], dtick=0.25, title=dict(text="Metric value", font=dict(size=12))))

    def write(self):
        self._figure.write_image(
            f"{self._config.model.performance_metrics.dir}/model_performance_metrics.png")
