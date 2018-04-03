#include "opencv2/opencv.hpp"
#include <opencv2/tracking.hpp>
#include <iostream>
#include <ctime>
#include "WindowTracker.h"

using namespace cv;
using namespace std;

static Rect2d bbox;

int main(int argc, char** argv)
{
	cout << " Using capture interface #0" << endl;

	waitKey(0);
	namedWindow("Display window", WINDOW_AUTOSIZE);

	/*VideoCapture cap("C:\\Users\\seitz\\Desktop\\objectTracking\\data\\chaplin.mp4");*/
	VideoCapture cap("democlip.mp4");
	//VideoCapture cap(0);
	if (!cap.isOpened())
		cout << " Failed to open capture interface";

	Mat frame;
	int i = 0;

	cap >> frame;

	bbox = Rect2d(280, 140, 150, 150);
	bbox = Rect2d(750, 170, 70, 70);
	Ptr<TrackerKCF> k = TrackerKCF::create();
	Ptr<WindowTracker> w = WindowTracker::create();

	bool res = w->init(frame, bbox);
	cout << "WindowTracker init " << res << endl;
	res = k->init(frame, bbox);
	cout << "TrackerKCF init " << res << endl;

	int cnt_every = 5;
	int crt_frame = 0;
	clock_t crt_begin = clock();

	for (;;)
	{
		if (++crt_frame == cnt_every) {
			cout << "fps: " << (cnt_every / (((double)(clock() - crt_begin)) / CLOCKS_PER_SEC)) << endl;
			crt_begin = clock();
			crt_frame = 0;
		}


		cap >> frame;
		if (frame.dims != 2) break;
		//cout << " Read frame #" << i++ << " " << frame.rows << "x" << frame.cols << endl;

		res = k->update(frame, bbox);
		rectangle(frame, bbox, Scalar(255, 0, 0));
		//cout << "TrackerKCF update " << res << endl;
/*
		res = w->update(frame, bbox);
		rectangle(frame, bbox, Scalar(255, 255, 0));*/
		//cout << "TrackerWindow update " << res << endl;

		imshow("Display window", frame);

		if (waitKey(1000) == 'q') break;
	}

	k.release();
	cap.release();

	//Mat image;
	//image = imread(argv[1], IMREAD_COLOR); // Read the file

	//if (!image.data) // Check for invalid input
	//{
	//	cout << "Could not open or find the image" << std::endl;
	//	return -1;
	//}

	//namedWindow("Display window", WINDOW_AUTOSIZE); // Create a window for display.
	//imshow("Display window", image); // Show our image inside it.

	//waitKey(0); // Wait for a keystroke in the window
	return 0;
}