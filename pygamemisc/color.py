colors = {"Black": (0, 0, 0), "White": (255, 255, 255), "Red": (255, 0, 0), "Cyan": (0, 255, 255),
          "Yellow": (255, 255, 0), "Pink": (255, 0, 255), "Green": (0, 128, 0), "Blue": (0, 0, 255),
          "Orange": (255, 165, 0)
          }
colorList = ["Red", "Cyan", "Yellow", "Pink", "Green", "Blue", "Orange"]


def colorTransformer(color):
    color = str(color).capitalize()
    try:
        return colors[color]
    except Exception as e:
        print(e)

def getNextColor(i):
    return colorList[i], colorTransformer(colorList[i])