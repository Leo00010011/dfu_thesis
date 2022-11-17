import open3d as o3d
import numpy as np


class RSReader:
    def start_camera(self):
        cfg = o3d.t.io.RealSenseSensorConfig(
            {'serial': '', 'color_format': 'RS2_FORMAT_RGB8', 'color_resolution': '1280,720', 'depth_resolution': '1280,720'})

        self.rs = o3d.t.io.RealSenseSensor()
        self.rs.init_sensor(cfg, 0, 'output/reconstruction/bagfile.bag')
        self.rs.start_capture()

    def get_frames(self):
        while True:
            im_rgbd = self.rs.capture_frame(True, True)
            color = np.array(im_rgbd.color)
            depth = np.array(im_rgbd.depth)
            yield color, depth

    def stop_camera(self):
        self.rs.stop_capture()

    def save_intrinsic(self):
        json_obj = str(self.rs.get_metadata())
        with open('output/reconstruction/intrinsic.json', 'w') as intrinsic_file:
            intrinsic_file.write(json_obj)
