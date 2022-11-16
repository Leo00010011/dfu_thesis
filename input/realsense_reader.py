import open3d as o3d
import numpy as np


class RSReader:
    def start_camera(self):
        cfg = o3d.t.io.RealSenseSensorConfig(
            {'serial': '', 'color_format': 'RS2_FORMAT_RGB8'})

        self.rs = o3d.t.io.RealSenseSensor()
        self.rs.init_sensor(cfg, 0)
        self.rs.start_capture()

    def get_frames(self):
        while True:
            im_rgbd = self.rs.capture_frame(True, True)
            color = np.array(im_rgbd.color)
            depth = np.array(im_rgbd.depth)
            yield color, depth

    def stop_camera(self):
        self.rs.stop_capture()
