import unittest

from elliottlib import util


class TestUtil(unittest.TestCase):
    def test_isolate_assembly_in_release(self):
        self.assertEqual(util.isolate_assembly_in_release('1.2.3-y.p.p1'), None)
        self.assertEqual(util.isolate_assembly_in_release('1.2.3-y.p.p1.assembly'), None)
        self.assertEqual(util.isolate_assembly_in_release('1.2.3-y.p.p1.assembly.x'), 'x')
        self.assertEqual(util.isolate_assembly_in_release('1.2.3-y.p.p1.assembly.xyz'), 'xyz')
        self.assertEqual(util.isolate_assembly_in_release('1.2.3-y.p.p1.assembly.xyz.el7'), 'xyz')

    def test_find_latest_builds(self):
        builds = [
            {"id": 13, "name": "a-container", "version": "v1.2.3", "release": "3.assembly.stream", "tag_name": "tag1"},
            {"id": 12, "name": "a-container", "version": "v1.2.3", "release": "2.assembly.hotfix_a", "tag_name": "tag1"},
            {"id": 11, "name": "a-container", "version": "v1.2.3", "release": "1.assembly.hotfix_a", "tag_name": "tag1"},
            {"id": 23, "name": "b-container", "version": "v1.2.3", "release": "3.assembly.test", "tag_name": "tag1"},
            {"id": 22, "name": "b-container", "version": "v1.2.3", "release": "2.assembly.hotfix_b", "tag_name": "tag1"},
            {"id": 21, "name": "b-container", "version": "v1.2.3", "release": "1.assembly.stream", "tag_name": "tag1"},
            {"id": 33, "name": "c-container", "version": "v1.2.3", "release": "3", "tag_name": "tag1"},
            {"id": 32, "name": "c-container", "version": "v1.2.3", "release": "2.assembly.hotfix_b", "tag_name": "tag1"},
            {"id": 31, "name": "c-container", "version": "v1.2.3", "release": "1", "tag_name": "tag1"},
        ]
        actual = util.find_latest_builds(builds, "stream")
        self.assertEqual([13, 21, 33], [b["id"] for b in actual])

        actual = util.find_latest_builds(builds, "hotfix_a")
        self.assertEqual([12, 21, 33], [b["id"] for b in actual])

        actual = util.find_latest_builds(builds, "hotfix_b")
        self.assertEqual([13, 22, 32], [b["id"] for b in actual])

        actual = util.find_latest_builds(builds, "test")
        self.assertEqual([13, 23, 33], [b["id"] for b in actual])

        actual = util.find_latest_builds(builds, None)
        self.assertEqual([13, 23, 33], [b["id"] for b in actual])

    def test_isolate_timestamp_in_release(self):
        actual = util.isolate_timestamp_in_release("foo-4.7.0-202107021813.p0.git.01c9f3f.el8")
        expected = "202107021813"
        self.assertEqual(actual, expected)

        actual = util.isolate_timestamp_in_release("foo-container-v4.7.0-202107021907.p0.git.8b4b094")
        expected = "202107021907"
        self.assertEqual(actual, expected)

        actual = util.isolate_timestamp_in_release("foo-container-v4.7.0-202107021907.p0.git.8b4b094")
        expected = "202107021907"
        self.assertEqual(actual, expected)

        actual = util.isolate_timestamp_in_release("foo-container-v4.8.0-202106152230.p0.git.25122f5.assembly.stream")
        expected = "202106152230"
        self.assertEqual(actual, expected)

        actual = util.isolate_timestamp_in_release("foo-container-v4.7.0-1.p0.git.8b4b094")
        expected = None
        self.assertEqual(actual, expected)

        actual = util.isolate_timestamp_in_release("foo-container-v4.7.0-202199999999.p0.git.8b4b094")
        expected = None
        self.assertEqual(actual, expected)

        actual = util.isolate_timestamp_in_release("")
        expected = None
        self.assertEqual(actual, expected)
