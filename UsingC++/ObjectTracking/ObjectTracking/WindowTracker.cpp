#include <opencv2/tracking.hpp>
#include <opencv2/opencv.hpp>
#include "WindowTracker.h"

using namespace cv;

void TrackerWindowModel::modelEstimationImpl(const std::vector<Mat>& responses) {

}

void TrackerWindowModel::modelUpdateImpl() {

}

Ptr<WindowTracker> WindowTracker::create() {
	return Ptr<WindowTracker>(new WindowTracker());
}

WindowTracker::WindowTracker(const WindowTracker::Params& parameters) : params(parameters) {
	isInit = false;
}

WindowTracker::Params::Params() {
	radius = 20;
}

bool WindowTracker::initImpl(const Mat& image, const Rect2d& boundingBox) {
	//sampler is the TrackerSampler
	TrackerSamplerCSC::Params CSCparameters;
	Ptr<TrackerSamplerAlgorithm> CSCSampler = new TrackerSamplerCSC(CSCparameters);
	if (!sampler->addTrackerSamplerAlgorithm(CSCSampler))
		return false;

	//featureSet is the TrackerFeatureSet
	TrackerFeatureHAAR::Params HAARparameters;
	Ptr<TrackerFeature> trackerFeature = new TrackerFeatureHAAR(HAARparameters);
	featureSet->addTrackerFeature(trackerFeature);

	model = new TrackerWindowModel();

	Mat image_;
	cvtColor(image, image_, COLOR_RGB2GRAY);
	expected = image_(boundingBox);
	last_bbox = boundingBox;

	return true;
}

bool WindowTracker::updateImpl(const Mat& image, Rect2d& boundingBox) {

	Mat image_;
	cvtColor(image, image_, COLOR_RGB2GRAY);

	long lowest_sum = -1;
	int best_x, best_y;

	for (int x = -params.radius; x <= params.radius; x++)
	{
		for (int y = -params.radius; y <= params.radius; y++)
		{
			int next_x = boundingBox.x + x;
			int next_y = boundingBox.y + y;

			Size s = image.size();
			if (next_x < 0 ||
				next_y < 0 ||
				next_x >= s.width ||
				next_y >= s.height) continue;

			Rect2d crt_bbox(next_x, next_y, boundingBox.width, boundingBox.height);
			Mat crt_cropped = image_(crt_bbox);
			Mat error_matrix;
			absdiff(expected, crt_cropped, error_matrix);
			long summed_error = sum(error_matrix)[0];

			if (lowest_sum == -1 || lowest_sum > summed_error) {
				best_x = x;
				best_y = y;
				lowest_sum = summed_error;
			}
		}
	}

	if (lowest_sum == -1) return false;

	last_bbox = Rect2d(boundingBox.x + best_x, boundingBox.y + best_y, boundingBox.width, boundingBox.height);
	expected = image_(last_bbox);


	boundingBox = last_bbox;

	return true;
}

void WindowTracker::read(const FileNode& fn) {

}

void WindowTracker::write(FileStorage& fs) const {

}