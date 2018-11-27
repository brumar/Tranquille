# Note that CPython will ignore all pragma's


# __pragma__('skip')
def __pragma__(*args, **kwargs) -> None:
    pass


# __pragma__('noskip')

__pragma__("skip")
# Another deviation from CPython is that the inclusion of a module has to be decided upon compiletime.
# This means that imports cannot be runtime conditional, so e.g. cannot be under an if.
# For compiletime conditional imports you can use __pragma__ (‘ifdef’).
# Also, since imports are resolved in one pass, cyclic imports are not supported.
alert = console = print
document = None

if False:
    from web import hello as back
    import sources.backend as eel

__pragma__("noskip")


async def frontcompute():
    a = document.getElementsByName("value_1")[0].value
    b = document.getElementsByName("value_2")[0].value
    v = await eel.compute(a, b)()
    console.log(v)
    document.getElementById("result").innerHTML = v


eel.expose(frontcompute)


def logdone():
    alert("this has been logged")


eel.expose(logdone)


def show_previous_results(lines):
    el = document.getElementById("previous")
    el.innerHTML = "<br/>".join(lines)

document.addEventListener("DOMContentLoaded", lambda e: eel.showpreviousvalues())

eel.expose(show_previous_results)
