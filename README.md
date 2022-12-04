# dot2png
A simple Flask-based application for rendering dot graphs as `.png` images.

### Requirements
This requires the python package Flask to run the application. It additionally requires graphviz and imagemagick. Specifically, the commands `dot` and `convert` should be available in your `$PATH`. This has been tested on Ubuntu 22.04.

### Running the application

The application is run by running `app.py`. Then, the content should be visible on `127.0.0.1:5000` in any web browser. Simply enter an equation into the text field and click the submit button.
