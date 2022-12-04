from flask import Flask, render_template, request, send_file
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

def RunCMD(cmd: str, timeout = 15):
    """
        Runs a command, captures stdout & stderr, trims output
        timeout: how long to let command run, -1 for infinite
    """

    proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    try:
        if timeout == -1:
            outs, errs = proc.communicate()
        else:
            outs, errs = proc.communicate(timeout=timeout)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()

    outs = outs.decode("UTF-8").strip()
    errs = (errs.decode("UTF-8").strip() if errs else None)

    return {"out": outs, "err": errs, "ret": proc.returncode}


app = Flask(__name__)


def save_file():
    # TODO: make this a non-blocking operation and update the page after the command executes if possible
    
    # steps:
    # 1. Create a file using the template
    f = open("graph.dot","w")
    f.write("digraph graphname {\n")
    
    graph = request.args.get("graph")
    f.write(graph)
    f.write("}\n")
    f.close()

    # 2. Convert to png
#    cmd = "dot graph.dot -T png -o static/graph.png"
    cmd = "dot graph.dot -T svg -o static/graph.svg"
    print("Executing: " + cmd)
    res = RunCMD(cmd, -1)
    if(not res["ret"]==0):
        print("Command exited with status: " + str(res["ret"]))
        if(res["out"]==None):
            res["out"]=""
        if(res["err"]==None):
            res["err"]=""
        print("Command stdout: " + res["out"])
        print("        stderr: " + res["err"])
        return render_template("index.html", graph_image="dot_failed.png", default_text=graph)
    
#    return render_template("index.html", graph_image="graph.png", default_text=graph)
    return render_template("index.html", graph_image="graph.svg", default_text=graph)

@app.route('/')
def index():
    if not request.args.get("graph"):
#        return render_template("index.html", graph_image="graph.png", default_text="hi")
        return render_template("index.html", graph_image="graph.svg", default_text="hi")

    return save_file()

if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0')
    app.run(debug=True, host='127.0.0.1')
