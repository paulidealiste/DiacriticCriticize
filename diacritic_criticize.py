import math
import random

import inkex


class DiacriticCriticize(inkex.EffectExtension):
    """Critical assessment of the supplied boring text"""

    def add_arguments(self, pars):  # type: (ArgumentParser) -> None
        pars.add_argument('--tab', help='Selected tab when ok is pressed')
        pars.add_argument('-d', '--decorations', default="chao")
        pars.add_argument('-q', '--quantity', default=5)

    def diacritic_glue(self, character, count):
        ldr = 0x0300
        udr = 0x036F
        siz = udr - ldr
        quantity = random.randint(2, count)
        for req in range(quantity):
            cp = ldr + math.floor(siz * random.random())
            char = chr(int(hex(cp), 16))
            character += char
        return character

    def diacritic_criticize(self, node, decorations, quantity):
        for elem in node:
            decorated = ''
            if decorations == 'diacritics':
                decorated = self.diacritics(elem.text, quantity)
            elif decorations == 'ravings':
                decorated = self.ravings(elem)
            elif decorations == 'chao':
                interim = self.ravings(elem)
                decorated = self.diacritics(interim, quantity)
        dcnodes = self.create_text(decorated, node)
        for child in dcnodes:
            node.getparent().append(child)

    def diacritics(self, text, quantity):
        criticized = [self.diacritic_glue(char, quantity) for char in text]
        return ''.join(criticized)

    def ravings(self, elem):
        include_ranges = [
            (0x0250, 0x02AF)
        ]
        alphabet = [chr(cp) for current_range in include_ranges for cp in range(current_range[0], current_range[1] + 1)]
        return ''.join(random.choice(alphabet) for i in range(len(elem.text)))

    def create_text(self, decorated, node):
        text = inkex.TextElement(**node.attrib)
        x = node.get('x')
        y = node.get('y')
        tspan = inkex.Tspan()
        tspan.set("sodipodi:role", "line")
        tspan.text = decorated
        text.set('x', str(x))
        text.set('y', str(y))
        text.append(tspan)
        return [text]

    def effect(self):  # type: () -> Any
        """Applies the effect"""
        decorations = self.options.decorations
        quantity = int(self.options.quantity)

        for elem in self.svg.selection.get(inkex.TextElement, inkex.FlowRoot):
            self.diacritic_criticize(elem, decorations, quantity)


if __name__ == '__main__':
    DiacriticCriticize().run()
