#include <opencv2/tracking.hpp>
#include <opencv2/opencv.hpp>

using namespace cv;

#pragma once

class TrackerWindowModel : public TrackerModel {
public:
	virtual ~TrackerWindowModel() {};
protected:
	void modelEstimationImpl(const std::vector<Mat>& responses);
	void modelUpdateImpl();
};

class WindowTracker : public Tracker {

public:
	struct Params {
		Params();
		int radius;
	};

	WindowTracker(const WindowTracker::Params& parameters = WindowTracker::Params());

	static Ptr<WindowTracker> WindowTracker::create();

	virtual ~WindowTracker() {}

	void read(const FileNode& fn);
	void write(FileStorage& fs) const;

protected:

	bool initImpl(const Mat& image, const Rect2d& boundingBox);
	bool updateImpl(const Mat& image, Rect2d& boundingBox);

private:
	Params params;
	Mat expected;
	Rect2d last_bbox;

};