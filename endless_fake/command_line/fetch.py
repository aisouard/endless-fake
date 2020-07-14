"""Endless Fake

Usage:
  endless-fake-fetch <output-dir>
  endless-fake-fetch (-h | --help)

Options:
  --output-dir PATH  Path to the download directory.
  -h --help          Show this screen.
  --version          Show version.
"""
import os
import urllib.request
from docopt import docopt

from .. import version

USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/80.0.3987.87 Safari/537.36"
ROOT_URL = "https://games.cdn.spilcloud.com/1562146373_EL-https"
FILES = [
    "game.min.js",
    "media/assets/bandera.json",
    "media/assets/bandera.png",
    "media/assets/brillito.json",
    "media/assets/brillito.png",
    "media/assets/cascada.json",
    "media/assets/cascada.png",
    "media/assets/char.png",
    "media/assets/estaticosD.json",
    "media/assets/estaticosD.png",
    "media/assets/flor.json",
    "media/assets/flor.png",
    "media/assets/fondo.jpg",
    "media/assets/FX-fusionB.json",
    "media/assets/FX-fusionB.png",
    "media/assets/gameover.png",
    "media/assets/gates-animados.json",
    "media/assets/gates-animados.png",
    "media/assets/GUI-BTNFX.json",
    "media/assets/GUI-BTNFX.png",
    "media/assets/GUI-gradiente.png",
    "media/assets/GUI-menu.json",
    "media/assets/GUI-menu.png",
    "media/assets/GUI-SHOP.png",
    "media/assets/HOWTO.jpg",
    "media/assets/juntador.json",
    "media/assets/juntador.png",
    "media/assets/moneda.json",
    "media/assets/moneda.png",
    "media/assets/monoA.json",
    "media/assets/monoA.png",
    "media/assets/monoB.json",
    "media/assets/monoB.png",
    "media/assets/monoB-splash.json",
    "media/assets/monoB-splash.png",
    "media/assets/monoC.json",
    "media/assets/monoC.png",
    "media/assets/monoC-splash.json",
    "media/assets/monoC-splash.png",
    "media/assets/monoD.json",
    "media/assets/monoD.png",
    "media/assets/monoD-splash.json",
    "media/assets/monoD-splash.png",
    "media/assets/monoE.json",
    "media/assets/monoE.png",
    "media/assets/monoE-splash.json",
    "media/assets/monoE-splash.png",
    "media/assets/monoF.json",
    "media/assets/monoF.png",
    "media/assets/monoF-splash.json",
    "media/assets/monoF-splash.png",
    "media/assets/monoG.json",
    "media/assets/monoG.png",
    "media/assets/monoG-splash.json",
    "media/assets/monoG-splash.png",
    "media/assets/monoH.json",
    "media/assets/monoH.png",
    "media/assets/monoH-splash.json",
    "media/assets/monoH-splash.png",
    "media/assets/monoI.json",
    "media/assets/monoI.png",
    "media/assets/monoI-splash.json",
    "media/assets/monoI-splash.png",
    "media/assets/monoJ.json",
    "media/assets/monoJ.png",
    "media/assets/monoJ-splash.json",
    "media/assets/monoJ-splash.png",
    "media/assets/niebla.png",
    "media/assets/nubes1.png",
    "media/assets/nubes2.png",
    "media/assets/numeros.json",
    "media/assets/numeros.png",
    "media/assets/pajaro.json",
    "media/assets/pajaro.png",
    "media/assets/pato-float.json",
    "media/assets/pato-float.png",
    "media/assets/portales.json",
    "media/assets/portales.png",
    "media/assets/retrybtn.png",
    "media/assets/selectormono.png",
    "media/assets/sombra.png",
    "media/assets/splash-monoA.json",
    "media/assets/splash-monoA.png",
    "media/assets/tap-to-play.png",
    "media/assets/unlockFX.json",
    "media/assets/unlockFX.png",
    "media/audio/coinA.ogg",
    "media/audio/INTRO-loopeada.ogg",
    "media/audio/loop-ingameB.ogg",
    "media/audio/SND-aleteo.ogg",
    "media/audio/SND-botonabajoA.ogg",
    "media/audio/SND-botonabajoB.ogg",
    "media/audio/SND-caeagua.ogg",
    "media/audio/SND-CAT-saltoA.ogg",
    "media/audio/SND-CAT-saltoB.ogg",
    "media/audio/SND-crow-saltoA.ogg",
    "media/audio/SND-crow-saltoB.ogg",
    "media/audio/SND-doblesalto.ogg",
    "media/audio/SND-DOG-saltoA.ogg",
    "media/audio/SND-DOG-saltoB.ogg",
    "media/audio/SND-elefante-saltoA.ogg",
    "media/audio/SND-elefante-saltoB.ogg",
    "media/audio/SND-florabre.ogg",
    "media/audio/SND-fusion.ogg",
    "media/audio/SND-gateA.ogg",
    "media/audio/SND-gateB.ogg",
    "media/audio/SND-morir.ogg",
    "media/audio/SND-nobuy.ogg",
    "media/audio/SND-play.ogg",
    "media/audio/SND-pollo-saltoA.ogg",
    "media/audio/SND-pollo-saltoB.ogg",
    "media/audio/SND-portalB.ogg",
    "media/audio/SND-rabbit-saltoA.ogg",
    "media/audio/SND-rabbit-saltoB.ogg",
    "media/audio/SND-rana-saltoA.ogg",
    "media/audio/SND-rana-saltoB.ogg",
    "media/audio/SND-robo-saltoA.ogg",
    "media/audio/SND-robo-saltoB.ogg",
    "media/audio/SND-salto.ogg",
    "media/audio/SND-seleccionmono.ogg",
    "media/audio/SND-TIGRE-saltoA.ogg",
    "media/audio/SND-TIGRE-saltoB.ogg",
    "media/buttons/mroegames.png",
    "media/blanco.jpg",
    "media/logo.png",
    "media/rotate.jpg",
    "index.html"
]

INDEX_HTML = """<html>
<body style="margin: 0;">
<iframe src="game.html" frameborder="0" width="360" height="640"></iframe>
</body>
</html>
"""

GAME_JS = """var GameAPI = {
    loadAPI: function (callback, SpilData) {
        callback({
            Award: {
                submit: function () {
                }
            },
            Branding: {
                displaySplashScreen: function (callback) {
                    callback();
                    return true;
                },
                getLink: function (ref) {
                    return {
                        action: function () {
                        }
                    };
                },
                getLogo: function () {
                    return {
                        image: "media/buttons/mroegames.png"
                    };
                }
            },
            GameBreak: {
                request: function (pauseCallback, resumeCallback) {
                    resumeCallback();
                    return true;
                }
            },
            Score: {
                submit: function () {
                }
            }
        });
    }
};
"""


def download_files(output_dir):
    urllib.request.URLopener.version = USER_AGENT

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    count = len(FILES)
    for i, file in enumerate(FILES):
        destpath = os.path.join(output_dir, *file.split("/"))
        if not os.path.isdir(os.path.dirname(destpath)):
            os.makedirs(os.path.dirname(destpath))

        print("Retrieving file {} of {}: {}".format(i, count, file))
        urllib.request.urlretrieve("{}/{}".format(ROOT_URL, file),
                                   os.path.join(output_dir, *file.split("/")))

    developer_js = os.path.join(output_dir, "developer.js")
    index_html = os.path.join(output_dir, "index.html")
    game_html = os.path.join(output_dir, "game.html")
    game_html_orig = os.path.join(output_dir, "game.html.orig")
    game_js = os.path.join(output_dir, "game.js")
    game_min_js = os.path.join(output_dir, "game.min.js")
    game_min_js_orig = os.path.join(output_dir, "game.min.js.orig")

    print("Renaming index.html to game.html")
    os.rename(index_html, game_html)

    print("Writing game.html.orig")
    with open(game_html, "r") as stream:
        data = stream.read()
    with open(game_html_orig, "w") as stream:
        stream.write(data)

    print("Writing game.min.js.orig")
    with open(game_min_js, "r") as stream:
        data = stream.read()
    with open(game_min_js_orig, "w") as stream:
        stream.write(data)

    print("Writing index.html")
    with open(index_html, "w") as stream:
        stream.write(INDEX_HTML)

    print("Writing game.js")
    with open(game_js, "w") as stream:
        stream.write(GAME_JS)

    print("Writing blank developer.js")
    open(developer_js, "a").close()


def main():
    args = docopt(__doc__, version=version, options_first=True)
    output_dir = args["<output-dir>"]
    download_files(output_dir)


if __name__ == "__main__":
    main()
