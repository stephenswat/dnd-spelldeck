import unittest
import generate


class TestStringMethods(unittest.TestCase):
    def test_nofilter(self):
        spells = generate.get_spells()
        self.assertEqual(len(spells), len(generate.SPELLS))


    def test_filter_class(self):
        spells = [x[0] for x in generate.get_spells(classes={"Warlock", "Fighter"})]
        self.assertIn("Alarm", spells)
        self.assertIn("Astral Projection", spells)
        self.assertNotIn("Augury", spells)

        spells = generate.get_spells(classes={"NotAClass"})
        self.assertEqual(len(spells), 0)


    def test_filter_schools(self):
        spells = [x[0] for x in generate.get_spells(schools={"Abjuration"})]
        self.assertIn("Alarm", spells)
        self.assertNotIn("Augury", spells)

        spells = [x[0] for x in generate.get_spells(schools={"NotASchool"})]
        self.assertNotIn("Alarm", spells)
        self.assertNotIn("Augury", spells)
        self.assertEqual(len(spells), 0)


    def test_filter_levels(self):
        spells = [x[0] for x in generate.get_spells(levels={0})]
        self.assertIn("Prestidigitation", spells)
        self.assertNotIn("Augury", spells)

        spells = [x[0] for x in generate.get_spells(levels={2})]
        self.assertIn("Augury", spells)
        self.assertNotIn("Prestidigitation", spells)

        spells = [x[0] for x in generate.get_spells(levels={0, 2})]
        self.assertIn("Augury", spells)
        self.assertIn("Prestidigitation", spells)

        self.assertEqual(len(generate.get_spells(levels={9000})), 0)


    def test_filter_names(self):
        spells = {x[0] for x in generate.get_spells(names={"Augury"})}
        self.assertEqual({"Augury"}, spells)

        spells = {x[0] for x in generate.get_spells(names={"Augury", "Prestidigitation"})}
        self.assertEqual({"Augury", "Prestidigitation"}, spells)
        self.assertEqual(len(spells), 2)

        spells = {x[0] for x in generate.get_spells(names={"NotASpell"})}
        self.assertEqual(set(), spells)


    def test_truncate(self):
        self.assertTrue(len(generate.truncate_string(generate.SPELLS['Animate Objects']['text'])) < generate.MAX_TEXT_LENGTH)
        if len(generate.SPELLS['Eldritch Blast']['text']) < generate.MAX_TEXT_LENGTH:
            self.assertEqual(generate.truncate_string(generate.SPELLS['Eldritch Blast']['text']), generate.SPELLS['Eldritch Blast']['text'])


    def test_parse_levels(self):
        self.assertEqual(generate.parse_levels(['1']), {1,})
        self.assertEqual(generate.parse_levels(['5', '8', '0']), {0, 5, 8})
        self.assertEqual(generate.parse_levels(['2-3']), {2, 3})
        self.assertEqual(generate.parse_levels(['2-6']), {2, 3, 4, 5, 6})
        self.assertEqual(generate.parse_levels(['0', '2-6', '9']), {0, 2, 3, 4, 5, 6, 9})


if __name__ == '__main__':
    unittest.main()
