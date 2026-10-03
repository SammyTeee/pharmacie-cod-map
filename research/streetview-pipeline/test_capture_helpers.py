"""Pure metadata/route checks: no browser inputs or network calls."""
import unittest
import firefox_capture as F
import walk_capture as W
class CaptureMetadataTests(unittest.TestCase):
    def test_panorama_angles_and_id(self):
        m=F.parse_url('https://www.google.com/maps/@52.6974696,-1.0751002,3a,90y,127.24h,95t/data=!3m5!1e1!3m3!1sGrczNc7jSfD4Nq3vGmGfDw!2e0')
        self.assertEqual(m['panorama_id'],'GrczNc7jSfD4Nq3vGmGfDw');self.assertEqual(m['pitch_degrees'],5);self.assertEqual(m['heading_degrees'],127.24)
    def test_place_id_is_not_panorama_id(self):
        m=F.parse_url('https://www.google.com/maps/place/Test/@52.7,-1.07,17z/data=!1s0x123:0x456!3d52.701!4d-1.071')
        self.assertNotIn('panorama_id',m);self.assertEqual(m['place_latitude'],52.701)
    def test_requested_view_is_distinct_from_resolved(self):
        m=F.parse_url('https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=52.7,-1.07&heading=180&pitch=-15&fov=80&pano=abc')
        self.assertNotIn('latitude',m);self.assertEqual(m['requested_latitude'],52.7);self.assertEqual(m['requested_pitch_degrees'],-15)
    def test_view_url_retains_position_panorama(self):
        original='https://www.google.com/maps/@52.7,-1.07,3a,90y,127h,95t/data=!1sabc!2e0'
        m=F.parse_url(W.url_view(F.parse_url(original),405,-12,50))
        self.assertEqual(m['panorama_id'],'abc');self.assertEqual(m['latitude'],52.7);self.assertEqual(m['heading_degrees'],45);self.assertEqual(m['pitch_degrees'],-12)
    def test_route_metrics(self):
        self.assertAlmostEqual(W.bearing((52.7,-1.07),(52.71,-1.07)),0,places=6)
        self.assertAlmostEqual(W.bearing((52.7,-1.07),(52.7,-1.06)),90,places=2)
        self.assertEqual(W.distance((52.7,-1.07),(52.7,-1.07)),0)
        self.assertTrue(1100<W.distance((52.7,-1.07),(52.71,-1.07))<1120)
    def test_legacy_encoded_angles_match_main_view(self):
        original='https://www.google.com/maps/@52.7,-1.07,3a,50y,135h,97t/data=!1sabc!6shttps:%2F%2Fexample.test%2Fthumbnail%3Fpitch%3D-7%26yaw%3D135!7i13312'
        view=W.url_view(F.parse_url(original),315,-15,80)
        self.assertIn('80y,315.00h,75.00t',view)
        self.assertIn('pitch%3D15.00%26yaw%3D315.00',view)
if __name__=='__main__':unittest.main()
