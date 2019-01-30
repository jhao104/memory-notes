异步编程适用于那些频繁读写文件和频繁与服务器交互数据的任务，异步程序以非阻塞的方式执行`I/O`操作。这样意味着程序可以在等待客户机返回数据的同时执行其他任务，而不是无所事事的等待，浪费资源和时间。

Python和其他许多编程一样，默认不具备异步特性。所幸的是，IT行业的快速发展，技术的不断更新，是我们可以编写异步程序。近年来，对速度的要求越来越高甚至超过了硬件能力。为此，世界各地的组织联合起来发表了《[反应式宣言](https://www.reactivemanifesto.org/)》

异步程序的非阻塞模式可以在Web应用程序的上下文中发挥显着的性能优势，有助于解决开发响应式应用程序中的问题。

Python3中加入了一些用于开发异步应用程序的强大模块，本文中将介绍一些工具，特别是与web开发相关的工具。

本文将试着开发一个基于 `aiohttp` 的简单反应式应用程序，根据用户给定的地理坐标，显示当前太阳系行星的天球坐标。

### Python中的异步

对于一些熟悉编写传统python代码的人来说，转换到异步程序可能有些不好接受。Python中的异步程序依赖于 **Coroutines(协程)** ，它与event loop（事件循环）一同工作，写出的代码像是执行多个小任务的片段。
协程可以看作是在代码中有一些带点函数，这些带点函数又是控制程序回调中的上下文，除了通过上下文交换数据，这些“yield”点还可以暂停和恢复协程执行。

事件循环决定了可以在任何指定时刻运行代码块—它负责协程之间的暂停、恢复和通信。 这意味着不同协程的最终可能以不同于它们之前被安排的顺序执行。 这种不按固定顺序运行不同代码块的想法称为异步。

可以在 `HTTP` 请求的场景中阐述异步的重要性。设想要向服务器发大量的请求。比如，要查询一个网站，以获得指定赛季所有运动员的统计信息。

我们可以按顺序依次发出每个请求。然而，对于每个请求，可以想象到可能会花一些时间等待上一个请求被发送到服务器，且收到服务器响应。

但是有时，这些无用的花销甚至可能需要几秒钟。因为程序可能会遇到网络延迟，访问数量过多，又或者是对方服务器的速度限制等问题。

如果我们的代码可以在等待服务器响应的同时做其他事情呢?而且，如果它只在响应数据到达后才处理返回数据呢?如果我们不必等到每个单独的请求都完成之后才继续处理列表中的下一个请求，那么我们可以快速地连续发出许多请求。

具有event loop的协程就可以让我们的代码支持以这样的形式运行。

### asyncio

[asyncio](https://docs.python.org/3/library/asyncio.html)是Python3.4版本引入的标准库,直接内置了对异步IO的支持。使用 `asyncio` 我们可以通过协程来完成某些任务，创建的协程(使用 `asyncio` 的语法 `asyncio.Task` 对象)只有在所有组成协程的任务完成执行后完成。

和其他异步编程语言不同，Python并不强制开发者使用语言自带的事件循环。正如[在Python 3.5中async/await是如何工作的](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/)指出的，Python协程构建的一个异步API允许我们使用任何事件循环。有些项目实现了完全不同的事件循环，比如[curio](https://curio.readthedocs.io/en/latest/tutorial.html)，或者允许为 `asyncio` 引入其他的事件循环策略(事件循环策略指是“在幕后”管理事件循环)，比如[uvloop](https://github.com/MagicStack/uvloop)。

使用 `asyncio` 并行运行两个协程的代码片段，每个协程在一秒钟后打印一条消息:
```python
# test.py
import asyncio

async def wait_around(n, name):
    for i in range(n):
        print(f"{name}: iteration {i}")
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(*[wait_around(2, "coroutine 0"), wait_around(5, "coroutine 1")])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

```

```python
jhaosMBP:Cenarius jhao$ time python test.py
coroutine 0: iteration 0
coroutine 1: iteration 0
coroutine 0: iteration 1
coroutine 1: iteration 1
coroutine 1: iteration 2
coroutine 1: iteration 3
coroutine 1: iteration 4

real    0m5.264s
user    0m0.078s
sys    0m0.043s
```

这段代码以异步方式大约5秒执行完毕。事件循环在遇到 `asyncio.sleep` 协程点时，会跳到其他代码继续执行。使用 `asyncio.gather` 告诉事件循环要调度两个 `wait_around` 实例。

`asyncio.gather` 接收一组“awaitables”(即协程或 `asyncio.Task`对象)，然后返回单个 `asyncio.Task`对像。其只在所有组成的 tasks/coroutines 完成时才完成。最后两行是 `asyncio` 的标准用法，用于运行指定的协程程序，直到执行完毕。

协程和函数不同，不会在调用后立即开始执行。`await` 关键字是用来告诉事件循环调度执行协同程序。

如果去掉 `asyncio.sleep` 前面的 `await`。程序几乎会立即完成，因为没有告诉事件循环要执行这个协程，在本例中，使用 `await` 调用协程使之休眠一段时间。

在了解了Python基本的异步代码之后，下面继续讨论web开发上的异步。

### 安装aiohttp

`aiohttp` 是用于处理异步 `HTTP` 请求的三方库。此外，它还提供了用于web服务的组件。可以通过 `pip` 安装 `aiohttp`，它要求Python版本大于3.5.3。

```bash
pip install aiohttp
```

#### 客户端:发送请求

下面的示例演示了如何使用 `aiohttp` 下载“baidu.com”网站的HTML内容:
```python
import asyncio
import aiohttp


async def make_request():
    url = "https://www.baidu.com"
    print(f"making request to {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                print(await resp.text())

loop = asyncio.get_event_loop()
loop.run_until_complete(make_request())

```

* 有几点需要强调：
 * 和前面的 `await asyncio.sleep` 一样，要获取HTML页面的内容,必须在 `resp.text()` 前面使用 `await` 。否则程序打印出来的内容会是这样：
```python
making request to https://www.baidu.com
<coroutine object ClientResponse.text at 0x109b8ddb0>
```

 * `async with` 是一个上下文管理器，它接收的是协程而不是函数。在这里的两处使用，是用于在内部自动关闭到服务器的连接释放资源。
 
 * `aiohttp.ClientSession` 具有和 `HTTP` 方法相同的方法，`session.get` 发送 **GET** 请求，`session.post` 发送 **POST** 请求。
 
这个例子本身并不比同步HTTP请求有多大性能优势。`aiohttp` 客户端真正优势在于多个请求并发：
```python
import asyncio
import aiohttp


async def make_request(session, req_n):
    url = "https://www.baidu.com"
    print(f"making request to {req_n} to {url}")
    async with session.get(url) as resp:
        if resp.status == 200:
            print(await resp.text())


async def main():
    n_request = 100
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[make_request(session, i) for i in range(n_request)])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

```
上面代码不是一个一个地发出请求，而是利用 `asyncio` 的 `asycio.gather` 实现并发。

### Web应用"行星定位"

下面将从头开始，开发一个web应用程序，报告用户所在位置上天空中行星的坐标(天象)。

我们使用[Geolocation API](https://www.w3schools.com/html/html5_geolocation.asp)来获取用户的当前位置。

#### PyEphem天象计算

一个天体的天象是指在地球上指定地点和时间观察到在天空中的位置。[PyEphem](https://rhodesmill.org/pyephem/)是一个计算精度很高的天文历算Python库。使用 `pip` 安装:

```bash
pip install ephem
```

使用 `Observer` 类计算格林威治某个时间点火星的天象(天体的高度和方位)：

```python
import ephem
import math


greenwich = ephem.Observer()
greenwich.lat = "51.4769"
greenwich.lon = "-0.0005"
greenwich.date = "2018/9/22 22:30:00"

mars = ephem.Mars()
mars.compute(greenwich)
az_deg, alt_deg = mars.az, mars.alt*convert

convert = math.pi / 180.
print(f"Mars当前的方位和高度为: {az_deg:.2f} {alt_deg:.2f}")
```

为了更加方便地获取行星的天象，我们写一个 `PlanetTracker` 类，带有一个返回指定行星当前高度和方位的方法。单位是度(PyEphem内部默认使用弧度而不是角度来表示度数值)

```python
# planet_tracker.py
import math
import ephem


class PlanetTracker(ephem.Observer):

    def __init__(self):
        super(PlanetTracker, self).__init__()
        self.planets = {
            "mercury": ephem.Mercury(),
            "venus": ephem.Venus(),
            "mars": ephem.Mars(),
            "jupiter": ephem.Jupiter(),
            "saturn": ephem.Saturn(),
            "uranus": ephem.Uranus(),
            "neptune": ephem.Neptune()
        }

    def calc_planet(self, planet_name, when=None):
        convert = 180. / math.pi
        if when is None:
            when = ephem.now()

        self.date = when
        if planet_name in self.planets:
            planet = self.planets[planet_name]
            planet.compute(self)
            return {
                "az": float(planet.az) * convert,
                "alt": float(planet.alt) * convert,
                "name": planet_name
            }
        else:
            raise KeyError(f"Couldn't find {planet_name} in planets dict")
```

这样就可以很方便地得到太阳系中其他七颗行星在任意地点的位置：

```python
tracker = PlanetTracker()
tracker.lat = "51.4769"
tracker.lon = "-0.0005"
print(tracker.calc_planet("mars"))
```

输出:

```python
{'az': 26.646611886328866, 'alt': -35.063254217502354, 'name': 'mars'}
```

#### aiohttp服务端

现在指定一组纬度和经度，我们可以得到行星当前的高度和方位。接下来，建立一个aiohttp服务，接收客户端发送的用户位置，返回其行星天象。

```python
# aiohttp_app.py
from aiohttp import web

from planet_tracker import PlanetTracker

routes = web.RouteTableDef()


@routes.get("/planets/{name}")
async def get_planet_ephmeris(request):
    planet_name = request.match_info['name']
    data = request.query
    try:
        geo_location_data = {
            "lon": str(data["lon"]),
            "lat": str(data["lat"]),
            "elevation": float(data["elevation"])
        }
    except KeyError as err:
        # 缺省 格林威治 Observatory
        geo_location_data = {
            "lon": "-0.0005",
            "lat": "51.4769",
            "elevation": 0.0,
        }
    print(f"get_planet_ephmeris: {planet_name}, {geo_location_data}")
    tracker = PlanetTracker()
    tracker.lon = geo_location_data["lon"]
    tracker.lat = geo_location_data["lat"]
    tracker.elevation = geo_location_data["elevation"]
    planet_data = tracker.calc_planet(planet_name)
    return web.json_response(planet_data)


app = web.Application()
app.add_routes(routes)

web.run_app(app, host="localhost", port=8000)
```

这里，给 `get_planet_ephmeris` 加上 `route.get` 装饰器以监听处理 `GET` 请求。

直接运行此py文件启动应用：
```bash
python aiohttp_app.py
```

成功启动后，在浏览器中访问 `http://localhost:8000/planets/mars` ，可以看到类似如下的响应内容:
```python
{"az": 98.72414165963292, "alt": -18.720718647020792, "name": "mars"}
```

你也可以使用 `curl` 命令进行测试:

```python
me@local:~$ curl localhost:8000/planets/mars  
{"az": 98.72414165963292, "alt": -18.720718647020792, "name": "mars"}
```

它响应给我们英国格林威治天文台的火星高度和方位。

也可以通过url参数传入经纬度位置，来获取其他地方的火星天象(注意使用引号将URL括起):

```python
me@local:~$ curl "localhost:8000/planets/mars?lon=145.051&lat=-39.754&elevation=0"  
{"az": 102.30273048280189, "alt": 11.690380174890928, "name": "mars"
```

这个还没有结束，`web.run_app` 函数是以阻塞的方式运行应用程序。这显然不是我们想要的方式!

要想以异步的形式运行起来，需要修改一点代码:
```python
# aiohttp_app.py
import asyncio
...

# web.run_app(app)

async def start_app():
    _runner = web.AppRunner(app)
    await _runner.setup()
    _site = web.TCPSite(
        _runner, "localhost", 8080
    )
    await _site.start()
    print(f"Serving up app on localhost:8080")
    return _runner, _site

loop = asyncio.get_event_loop()
runner, site = loop.run_until_complete(start_app())
try:
    loop.run_forever()
except KeyboardInterrupt as err:
    loop.run_until_complete(runner.cleanup())
```

注意这里使用的是 `loop.run_forever`，而不是前面的 `loop.run_until_complete`。因为这里并不是为了执行一定数量的协程，而是希望我们的服务挂起处理请求，直到使用 `ctrl+c` 退出，这时才优雅地关闭服务器。

#### 前端 HTML/JavaScript

`aiohttp` 支持加载HTML和JavaScript文件。但是并不鼓励使用 `aiohttp` 服务加载CSS和JavaScript等"静态"资源，但是我们这里只是做一个演示程序。

接下来 `aiohttp_app.py` 添加几行代码。加载JavaScript文件的HTML文件:

```python
# aiohttp_app.py
...
@routes.get('/')
async def hello(request):  
    return web.FileResponse("./index.html")


app = web.Application()  
app.add_routes(routes)  
app.router.add_static("/", "./")  
...
```

`hello` 协程监听 `localhost:8000/` 上的`GET` 请求，返回 `index.html`。该文件位于运行服务的同目录下。项目目录结构:

```python
--aiphttp_api.py
--app.js
--index.html
--planet_tracker.py
```

`app.router.add_static` 这一行行声明在 `localhost:8000/` 上设置了一个路由，用于在运行服务器的同目录中加载静态文件。这样浏览器将才能够找到在 `index.html` 中引用的JavaScript文件。

**注意：**在生产环境中，务必将HTML、CSS和JS文件放到单独的目录中。这样可以避免一些好奇的用户访问服务器上的代码。

`index.html` 内容非常简单:

```python
<!DOCTYPE html>  
<html lang='en'>

<head>  
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Planet Tracker</title>
</head>  
<body>  
    <div id="app">
        <label id="lon">Longitude: <input type="text"/></label><br/>
        <label id="lat">Latitude: <input type="text"/></label><br/>
        <label id="elevation">Elevation: <input type="text"/></label><br/>
    </div>
    <script src="/app.js"></script>
</body>  
```

不过，`app.js` 文件稍微复杂一些:

```python
var App = function() {

    this.planetNames = [
        "mercury",
        "venus",
        "mars",
        "jupiter",
        "saturn",
        "uranus",
        "neptune"
    ]

    this.geoLocationIds = [
        "lon",
        "lat",
        "elevation"
    ]

    this.keyUpInterval = 500
    this.keyUpTimer = null
    this.planetDisplayCreated = false
    this.updateInterval = 2000 // update very second and a half
    this.updateTimer = null
    this.geoLocation = null

    this.init = function() {
        this.getGeoLocation().then((position) => {
            var coords = this.processCoordinates(position)
            this.geoLocation = coords
            this.initGeoLocationDisplay()
            this.updateGeoLocationDisplay()
            return this.getPlanetEphemerides()
        }).then((planetData) => {
            this.createPlanetDisplay()
            this.updatePlanetDisplay(planetData)
        }).then(() => {
            return this.initUpdateTimer()
        })
    }

    this.update = function() {
        if (this.planetDisplayCreated) {
            this.getPlanetEphemerides().then((planetData) => {
                this.updatePlanetDisplay(planetData)
            })
        }
    }

    this.get = function(url, data) {
        var request = new XMLHttpRequest()
        if (data !== undefined) {
            url += `?${data}`
        }
        // console.log(`get: ${url}`)
        request.open("GET", url, true)
        return new Promise((resolve, reject) => {
            request.send()
            request.onreadystatechange = function(){
                if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                    resolve(this)
                }
            }
            request.onerror = reject
        })
    }

    this.processCoordinates = function(position) {
        var coordMap = {
            'longitude': 'lon',
            'latitude': 'lat',
            'altitude': 'elevation'
        }
        var coords = Object.keys(coordMap).reduce((obj, name) => {
            var coord = position.coords[name]
            if (coord === null || isNaN(coord)) {
                coord = 0.0
            }
            obj[coordMap[name]] = coord
            return obj
        }, {})
        return coords
    }

    this.coordDataUrl = function (coords) {
        postUrl = Object.keys(coords).map((c) => {
            return `${c}=${coords[c]}`
        })
        return postUrl
    }

    this.getGeoLocation = function() {
        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve)
        })
    }

    this.getPlanetEphemeris = function(planetName) {
        var postUrlArr = this.coordDataUrl(this.geoLocation)
        return this.get(`/planets/${planetName}`, postUrlArr.join("&")).then((req) => {
            return JSON.parse(req.response)
        })
    }

    this.getPlanetEphemerides = function() {
        return Promise.all(
            this.planetNames.map((name) => {
                return this.getPlanetEphemeris(name)
            })
        )
    }

    this.createPlanetDisplay = function() {
        var div = document.getElementById("app")
        var table = document.createElement("table")
        var header = document.createElement("tr")
        var headerNames = ["Name", "Azimuth", "Altitude"]
        headerNames.forEach((headerName) => {
            var headerElement = document.createElement("th")
            headerElement.textContent = headerName
            header.appendChild(headerElement)
        })
        table.appendChild(header)
        this.planetNames.forEach((name) => {
            var planetRow = document.createElement("tr")
            headerNames.forEach((headerName) => {
                planetRow.appendChild(
                    document.createElement("td")
                )
            })
            planetRow.setAttribute("id", name)
            table.appendChild(planetRow)
        })
        div.appendChild(table)
        this.planetDisplayCreated = true
    }

    this.updatePlanetDisplay = function(planetData) {
        planetData.forEach((d) => {
            var content = [d.name, d.az, d.alt]
            var planetRow = document.getElementById(d.name)
            planetRow.childNodes.forEach((node, idx) => {
                var contentFloat = parseFloat(content[idx])
                if (isNaN(contentFloat)) {
                    node.textContent = content[idx]
                } else {
                    node.textContent = contentFloat.toFixed(2)
                }
            })
        })
    }

    this.initGeoLocationDisplay = function() {
        this.geoLocationIds.forEach((id) => {
            var node = document.getElementById(id)
            node.childNodes[1].onkeyup = this.onGeoLocationKeyUp()
        })
        var appNode = document.getElementById("app")
        var resetLocationButton = document.createElement("button")
        resetLocationButton.setAttribute("id", "reset-location")
        resetLocationButton.onclick = this.onResetLocationClick()
        resetLocationButton.textContent = "Reset Geo Location"
        appNode.appendChild(resetLocationButton)
    }

    this.updateGeoLocationDisplay = function() {
        Object.keys(this.geoLocation).forEach((id) => {
            var node = document.getElementById(id)
            node.childNodes[1].value = parseFloat(
                this.geoLocation[id]
            ).toFixed(2)
        })
    }

    this.getDisplayedGeoLocation = function() {
        var displayedGeoLocation = this.geoLocationIds.reduce((val, id) => {
            var node = document.getElementById(id)
            var nodeVal = parseFloat(node.childNodes[1].value)
            val[id] = nodeVal
            if (isNaN(nodeVal)) {
                val.valid = false
            }
            return val
        }, {valid: true})
        return displayedGeoLocation
    }

    this.onGeoLocationKeyUp = function() {
        return (evt) => {
            // console.log(evt.key, evt.code)
            var currentTime = new Date()
            if (this.keyUpTimer !== null){
                clearTimeout(this.keyUpTimer)
            }
            this.keyUpTimer = setTimeout(() => {
                var displayedGeoLocation = this.getDisplayedGeoLocation()
                if (displayedGeoLocation.valid) {
                    delete displayedGeoLocation.valid
                    this.geoLocation = displayedGeoLocation
                    console.log("Using user supplied geo location")
                }
            }, this.keyUpInterval)
        }
    }

    this.onResetLocationClick = function() {
        return (evt) => {
            console.log("Geo location reset clicked")
            this.getGeoLocation().then((coords) => {
                this.geoLocation = this.processCoordinates(coords)
                this.updateGeoLocationDisplay()
            })
        }
    }

    this.initUpdateTimer = function () {
        if (this.updateTimer !== null) {
            clearInterval(this.updateTimer)
        }
        this.updateTimer = setInterval(
            this.update.bind(this),
            this.updateInterval
        )
        return this.updateTimer
    }

    this.testPerformance = function(n) {
        var t0 = performance.now()
        var promises = []
        for (var i=0; i<n; i++) {
            promises.push(this.getPlanetEphemeris("mars"))
        }
        Promise.all(promises).then(() => {
            var delta = (performance.now() - t0)/1000
            console.log(`Took ${delta.toFixed(4)} seconds to do ${n} requests`)
        })
    }
}

var app  
document.addEventListener("DOMContentLoaded", (evt) => {  
    app = new App()
    app.init()
})
```

该应用程序将定时(间隔2秒)更新显示行星的方位和高度信息。`Web Geolocation API` 会默认读取用户当前地理位置，也可以自己手动输入地理坐标置。如果用户停止输入半秒以上时间，就会开始自动更新行星位置数据。

![](http://qiniu.spiderpy.cn/19-1-4/1202956.jpg)

虽然这不是JavaScript教程，但是这里可以简单讲解下JS脚本的部分内容:

* `createPlanetDisplay` 动态创建HTML元素并绑定到Document Object Model(DOM);

* `updatePlanetDisplay` 用来从服务器接收数据，使用 `createPlanetDisplay` 显示；

* `getGeoLocation` 使用 [Web Geolocation API](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API) 获取用户当前的地理坐标。但要求在“安全的上下文中”使用(即必须使用HTTPS而不是HTTP)

* `getPlanetEphemeris` 和 `getPlanetEphemerides` 都是向服务器发出GET请求，分别获取指定行星和所有行星的位置信息。

### 结语

在本文中，简单介绍了Python中的异步web开发是什么样子的——它的优点和用途。之后，构建了一个简单的基于 `aiohttp` 的响应式应用程序，在用户给定地理坐标的情况下，动态显示当前太阳系行星的相关天空位置。