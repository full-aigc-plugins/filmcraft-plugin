"""字幕精度回归，覆盖实际发现的帧网格损失和输入保护。"""
import importlib.util
from pathlib import Path
import tempfile
import unittest
p=Path(__file__).resolve().parents[1]/'skills/filmcraft-subtitle-delivery/scripts/sync_srt.py'
s=importlib.util.spec_from_file_location('subtitle_sync',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class SubtitleSync(unittest.TestCase):
    def test_bom_multiline_and_exact_milliseconds(self):
        cues=m.parse_cues('\ufeff7\r\n00:00:01,123 --> 00:00:02,487\r\n第一句\r\nHello, world.\r\n')
        self.assertEqual(cues,[{'startMs':1123,'endMs':2487,'text':'第一句\nHello, world.'}])
    def test_frame_quantized_shift_is_not_accepted_as_precise(self):
        cues=[{'startMs':1123,'endMs':2487,'text':'A'}]
        with self.assertRaisesRegex(ValueError,'precision'):
            m.verify_track(cues,[{'start':1620*m.TICKS_PER_MS,'end':2980*m.TICKS_PER_MS,'text':'A'}],500)
    def test_repair_uses_real_caption_id_and_end_before_start(self):
        cues=[{'startMs':1123,'endMs':2487,'text':'A'}]
        steps=m.repair_steps(cues,[{'id':91,'start':1120*m.TICKS_PER_MS,'end':2480*m.TICKS_PER_MS,'text':'A'}])
        self.assertEqual([(s['params']['caption'],s['params']['edge'],s['params']['delta']) for s in steps],[(91,'out',7*m.TICKS_PER_MS),(91,'in',3*m.TICKS_PER_MS)])
    def test_negative_offset_rejected_before_output_or_cli(self):
        with tempfile.TemporaryDirectory() as t:
            source=Path(t)/'input.srt';source.write_text('1\n00:00:00,123 --> 00:00:01,000\nA\n');out=Path(t)/'result'
            with self.assertRaisesRegex(ValueError,'zero'):m.sync('unavailable-cli',source,out,-500)
            self.assertFalse(out.exists());self.assertTrue(source.exists())
    def test_malformed_and_reversed_cues_rejected(self):
        for text in ['', '1\n00:00:02,000 --> 00:00:01,000\nA', '1\n00:99:00,000 --> 01:00:00,000\nA']:
            with self.subTest(text=text),self.assertRaises(ValueError):m.parse_cues(text)
    def test_text_changes_cannot_be_hidden_by_correct_timing(self):
        with self.assertRaisesRegex(ValueError,'text'):m.repair_steps([{'startMs':0,'endMs':1000,'text':'完整字幕'}],[{'id':5,'start':0,'end':1000*m.TICKS_PER_MS,'text':'字幕'}])
    def test_display_index_can_change_but_protected_contents_cannot(self):
        before=[{'id':10,'label':'C1','name':'Reference','captions':[{'id':11,'text':'Keep','start':0,'end':1000}]}]
        after=[{'id':12,'label':'C1','name':'New','captions':[]},dict(before[0],label='C2')]
        m.verify_protected_tracks(before,after,12)
        after[1]=dict(after[1],name='Clobbered')
        with self.assertRaisesRegex(ValueError,'Non-target'):m.verify_protected_tracks(before,after,12)
    def test_relative_media_is_resolved_against_source_project(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);project=root/'source.fcproj';project.touch();media=root/'shot.avi';media.write_bytes(b'fixture')
            previous=m.execute;calls=[]
            def read(cli,*args):
                calls.append(args)
                return '{"rows":[{"item":31}]}' if 'project.items' in args else '{"fields":[{"name":"File Path","value":"shot.avi"}]}'
            try:
                m.execute=read;steps=m.media_relinks('cli',project)
            finally:m.execute=previous
            self.assertEqual(steps,[{'id':'media.relink','params':{'item':31,'path':str(media.resolve()),'relinkOthers':False,'alignTimecode':False}}])
            self.assertTrue(all(str(project) in args for args in calls))
if __name__=='__main__':unittest.main()
