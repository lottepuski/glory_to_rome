import svgwrite
from svgwrite import cm, mm, container

ORIGIN_X = 10
ORIGIN_Y = 10
ORIGIN = (ORIGIN_X, ORIGIN_Y)


class Rectangle(object):
    CENTER_RECT = (5 * cm, 5 * cm)
    SIZE_RECT = (60 * mm, 90 * mm)
    RX = 8 * mm
    RY = 8 * mm
    FILL = 'white'
    STROKE = 'black'
    STROKE_WIDTH = 1.5

    def __init__(self, dwg, insert=CENTER_RECT, size=SIZE_RECT, rx=RX, ry=RY,
                 fill=FILL, stroke=STROKE, stroke_width=STROKE_WIDTH):
        self.base = dwg.rect(insert=insert, size=size, rx=rx, ry=ry,
                             fill=fill, stroke=stroke,
                             stroke_width=stroke_width)


class Card(svgwrite.container.Group):
    def __init__(self, dwg, name="Card", insert=ORIGIN, fill='white', color='green', material_name="Wood",
                 role_name="Craftsman"):
        """
        :param dwg: svgwrite.Drawing
        :param name: Name of the card
        :param insert: Insert location in mm. type: int
        :param fill: Color
        """
        if len(name.split(" ")) > 1:
            tmp_id = "_".join(name.split(" "))
        else:
            tmp_id = name
        super(Card, self).__init__(id=tmp_id, fill=fill)
        self.dwg = dwg
        self.insert = (insert[0] * mm, insert[1] * mm)
        self.name = name
        self.color = color
        self.material_name = material_name
        self.role_name = role_name

        self.base = Rectangle(dwg, insert=self.insert).base

        # Locations - Card specific
        self.title_x = insert[0] + 15
        self.title_y = insert[1] + 10
        self.role_x = 4
        self.role_y = 10
        self.material_x = 33
        self.material_y = 87
        self.coin_one_x = 6 + insert[0]
        self.coin_one_y = 84 + insert[1]

    def draw(self):
        title = self.make_title()
        role = self.make_role(self.role_name)
        material = self.make_material(self.material_name)
        coins = self.make_coins()
        self.add(self.base)
        self.add(title)
        self.add(role)
        self.add(material)
        for coin in coins:
            self.add(coin)

    def make_title(self):
        words = self.name.split(" ")
        title_loc = (self.title_x * mm, self.title_y * mm)
        if len(words) == 1:
            title = self.dwg.text(self.name.upper(),
                                  x=[title_loc[0]], y=[title_loc[1]],
                                  style="font-size:24px; font-family:Arial",
                                  fill='black', stroke='black')
        else:
            title = self.dwg.text("",
                                  x=[title_loc[0]], y=[title_loc[1]],
                                  style="font-size:24px;" +
                                        "font-family:Arial;" +
                                        "display-align:center",
                                  fill='black', stroke='black')
            for ix, word in enumerate(words):
                title_loc = (self.title_x * mm, (self.title_y + 7*ix) * mm)
                tword = self.dwg.tspan(word.upper(),
                                       x=[title_loc[0]], y=[title_loc[1]])
                title.add(tword)
        return title

    def make_coins(self):
        """
        :return: coins in the order 1st outer, 1st inner, 2nd outer, 2nd inner ...
        """
        return self.make_one_coin()

    def make_one_coin(self):
        coin_one_center = (self.coin_one_x * mm, self.coin_one_y * mm)
        coin_color = 'darkgoldenrod'
        coin_outer = self.dwg.circle(center=coin_one_center, r=6 * mm, stroke=coin_color,
                                     stroke_width=2)
        coin_inner = self.dwg.circle(center=coin_one_center, r=5 * mm, stroke=coin_color,
                                     stroke_width=2)
        return coin_outer, coin_inner

    def make_role(self, role_name):
        role_loc = (self.role_x * mm, self.role_y * mm)
        role = self.dwg.text(role_name.upper(), insert=self.insert, dx=[role_loc[0]], dy=[role_loc[1]],
                             style="font-size:24px;" +
                                   "font-family:Arial;" +
                                   "writing-mode:tb;" +
                                   "glyph-orientation-vertical:0",
                             fill=self.color,
                             stroke=self.color)
        return role

    def make_material(self, material_name):
        material_loc = (self.material_x * mm, self.material_y * mm)
        material = self.dwg.text(material_name.upper(), insert=self.insert,
                                 dx=[material_loc[0]], dy=[material_loc[1]],
                                 style="font-size:24px; font-family:Arial",
                                 fill=self.color, stroke=self.color)
        return material


class Craftsman(Card):
    def __init__(self, dwg, name="Card", insert=ORIGIN, fill='white', color='green'):
        super(Craftsman, self).__init__(dwg=dwg, name=name, insert=insert, fill=fill, color=color)
        self.material_name = "Wood"
        self.role_name = "Craftsman"
        self.draw()


class Laborer(Card):
    def __init__(self, dwg, name="Card", insert=ORIGIN, fill='white', color='gold'):
        super(Laborer, self).__init__(dwg=dwg, name=name, insert=insert, fill=fill, color=color),
        self.material_name = "Rubble"
        self.role_name = "Laborer"
        self.material_x = 30
        self.role_y = 20
        self.draw()


class Architect(Card):
    def __init__(self, dwg, name="Card", insert=ORIGIN, fill='white', color='slategrey'):
        super(Architect, self).__init__(dwg=dwg, name=name, insert=insert, fill=fill, color=color),
        self.material_name = "Concrete"
        self.role_name = "Architect"
        self.material_x = 21
        self.draw()

    def make_coins(self):
        one_outer, one_inner = self.make_one_coin()
        self.coin_one_x += 4
        two_outer, two_inner = self.make_one_coin()
        return one_outer, one_inner, two_outer, two_inner


class Legionary(Card):
    def __init__(self, dwg, name="Card", insert=ORIGIN, fill='white', color='firebrick'):
        super(Legionary, self).__init__(dwg=dwg, name=name, insert=insert, fill=fill, color=color),
        self.material_name = "Brick"
        self.role_name = "Legionary"
        # self.material_x = 21
        self.draw()

    def make_coins(self):
        one_outer, one_inner = self.make_one_coin()
        self.coin_one_x += 4
        two_outer, two_inner = self.make_one_coin()
        return one_outer, one_inner, two_outer, two_inner


class Patron(Card):
    def __init__(self, dwg, name="Card", insert=ORIGIN, fill='white', color='purple'):
        super(Patron, self).__init__(dwg=dwg, name=name, insert=insert, fill=fill, color=color),
        self.material_name = "Marble"
        self.role_name = "Patron"
        self.material_x = 30
        self.role_y = 20
        self.draw()

    def make_coins(self):
        one_outer, one_inner = self.make_one_coin()
        self.coin_one_x += 4
        two_outer, two_inner = self.make_one_coin()
        self.coin_one_x += 4
        three_outer, three_inner = self.make_one_coin()
        return one_outer, one_inner, two_outer, two_inner, three_outer, three_inner


class Merchant(Card):
    def __init__(self, dwg, name="Card", insert=ORIGIN, fill='white', color='cornflowerblue'):
        super(Merchant, self).__init__(dwg=dwg, name=name, insert=insert, fill=fill, color=color),
        self.material_name = "Stone"
        self.role_name = "Merchant"
        # self.material_x = 21
        self.role_y = 15
        self.draw()

    def make_coins(self):
        one_outer, one_inner = self.make_one_coin()
        self.coin_one_x += 4
        two_outer, two_inner = self.make_one_coin()
        self.coin_one_x += 4
        three_outer, three_inner = self.make_one_coin()
        return one_outer, one_inner, two_outer, two_inner, three_outer, three_inner


def basic_shapes(name):
    dwg = svgwrite.Drawing(filename=name, debug=True)
    circus = Craftsman(dwg=dwg, insert=(10, 10), name="Circus")
    palisade = Craftsman(dwg=dwg, insert=(90, 10), name="Palisade")
    bar = Laborer(dwg=dwg, insert=(180, 10), name="Bar")
    road = Laborer(dwg=dwg, insert=(270, 10), name="Road")
    tower = Architect(dwg=dwg, insert=(10, 110), name="Tower")
    aqueduct = Architect(dwg=dwg, insert=(90, 110), name="Aqueduct")
    archway = Legionary(dwg=dwg, insert=(180, 110), name="Archway")
    bath = Legionary(dwg=dwg, insert=(270, 110), name="Bath")
    forum = Patron(dwg=dwg, insert=(10, 210), name="forum")
    basilica = Patron(dwg=dwg, insert=(90, 210), name="Basilica")
    coliseum = Merchant(dwg=dwg, insert=(180, 210), name="Coliseum")
    circus_max = Merchant(dwg=dwg, insert=(270, 210), name="Circus Maximus")

    dwg.add(circus)
    dwg.add(palisade)
    dwg.add(bar)
    dwg.add(road)
    dwg.add(tower)
    dwg.add(aqueduct)
    dwg.add(archway)
    dwg.add(bath)
    dwg.add(forum)
    dwg.add(basilica)
    dwg.add(coliseum)
    dwg.add(circus_max)
    dwg.save()


if __name__ == '__main__':
    basic_shapes('card.svg')
