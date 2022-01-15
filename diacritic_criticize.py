import math
import random

import inkex


class DiacriticCriticize(inkex.EffectExtension):
    """Critical assessment of the supplied boring text"""
    UTF8_Ranges = {
        "LatinExtendedA": (0x0100, 0x017F),
        "LatinExtendedB": (0x0180, 0x024F),
        "IPAExtensions": (0x0250, 0x02AF),
        "GreekAndCoptic": (0x0370, 0x03FF),
        "Cyrillic": (0x0400, 0x04FF),
        "CyrillicSupplement": (0x0500, 0x052F),
        "MathematicalOperations": (0x2200, 0x22FF),
        "LegacyComputing": (0x1FB00, 0x1FBFF),
        "Cuneiform": (0x12000, 0x123FF)
    }

    def add_arguments(self, pars):  # type: (ArgumentParser) -> None
        pars.add_argument('--tab', help='Selected tab when ok is pressed')
        pars.add_argument('-d', '--decorations', default="chao")
        pars.add_argument('-q', '--quantity', default=5)
        pars.add_argument('-u8r', '--utf8range', default="IPAExtensions")

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
        include_ranges = self.fill_utf8ranges()
        alphabet = [chr(cp) for current_range in include_ranges for cp in range(current_range[0], current_range[1] + 1)]
        return ''.join(random.choice(alphabet) for i in range(len(elem.text)))

    def fill_utf8ranges(self):
        return [self.UTF8_Ranges.get(self.options.utf8range)]

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
