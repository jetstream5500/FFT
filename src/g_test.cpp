#include <iostream>
#include <fstream>
#include <cmath>

using namespace std;

const double xmin = -10;
const double xmax = 10;
const double ymin = -10;
const double ymax = 10;
const int width = 300;
const int height = 300;

struct Point {
  double x;
  double y;
};

void data_generation(Point data[]) {
  for (int i = 0; i<width; i++) {
    double mapped_i = i*((xmax-xmin)/width);
    Point p = {mapped_i, sin(mapped_i)};
    data[i] = p;
  }
}

int main() {
  ofstream plot("graph.ppm");
  plot << "P3" << endl;
  plot << width << " " << height << endl;
  plot << "255" << endl;

  Point data[width];
  data_generation(data);

  for (int i = 0; i<width; i++) {
    cout << "(" << data[i].x << ", " << data[i].y << ") ";
  }
  cout << endl;

  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      int r = 255;
      int g = 255;
      int b = 255;
      plot << r << " " << g << " " << b << endl;
    }
  }

  //system("open graph.ppm");
  return 0;
}
