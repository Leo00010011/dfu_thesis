import open3d as o3d
import pyrealsense2 as rs
import numpy as np


class RSReader:
    def start_camera(self):
        if not o3d.t.io.RealSenseSensor.list_devices():
            raise Exception("Camera unavailable")
        cfg = o3d.t.io.RealSenseSensorConfig(
            {'serial': '', 'color_format': 'RS2_FORMAT_RGB8', 'color_resolution': '1280,720', 'depth_resolution': '1280,720'})

        self.rs = o3d.t.io.RealSenseSensor()
        self.rs.init_sensor(cfg, 0, 'output/reconstruction/bagfile.bag')
        self.rs.start_capture(False)

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

    def get_resolution(self):
        return (self.rs.get_metadata().height,
                self.rs.get_metadata().width)


class RSPlayback:
    def start_camera(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_device_from_file('bags_to_process/a.bag')
        self.profile = self.pipeline.start(self.config)
        self.stream_color = self.profile.get_stream(rs.stream.color)
        self.stream_depth = self.profile.get_stream(rs.stream.depth)
        self.device = self.profile.get_device()
        self.playback = self.device.as_playback()
        

    def get_frames(self):
        align = rs.align(rs.stream.color)
        while True:
            frames = self.pipeline.wait_for_frames()
            frames = align.process(frames)
            color_frame = frames.get_color_frame()
            color_frame = np.asanyarray(color_frame.get_data())
            depth_frame = frames.get_depth_frame()
            depth_frame = np.asanyarray(depth_frame.get_data())
            yield color_frame, depth_frame



    def stop_camera(self):
        self.pipeline.stop()

    def get_resolution(self):
        return (self.stream_color.as_video_stream_profile().intrinsics.height,
                self.stream_color.as_video_stream_profile().intrinsics.width)
        

    def save_intrinsic(self):
        bag_reader = o3d.t.io.RSBagReader()
        bag_reader.open("bags_to_process/a.bag")
        json_obj = str(bag_reader.metadata)
        with open('output/reconstruction/intrinsic.json', 'w') as intrinsic_file:
            intrinsic_file.write(json_obj)
        bag_reader.close()


    
