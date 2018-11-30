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
import backend
__pragma__("noskip")


async def frontcompute():
    a = document.getElementsByName("value_1")[0].value
    b = document.getElementsByName("value_2")[0].value
    v = await backend.compute(a, b)()
    console.log(v)
    document.getElementById("result").innerHTML = v


def logdone():
    console.log("this has been logged")



def show_previous_results(lines):
    el = document.getElementById("previous")
    el.innerHTML = "<br/>".join(lines)

document.addEventListener("DOMContentLoaded", lambda e: backend.showpreviousvalues())

