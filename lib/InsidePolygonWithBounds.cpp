//SOLUTION #1 (2D) - Redesigned

#include <math.h>
#include <iostream>


#define MIN(x,y) (x < y ? x : y)
#define MAX(x,y) (x > y ? x : y)

#define INSIDE    1
#define OUTSIDE   0

struct Point
{
    Point() : x(.0), y(.0) {};

    Point(double x1, double y1) : x(x1), y(y1) {};

    bool operator==(const Point& _right)
    {
        return x == _right.x && y == _right.y;
    };

    double x, y;
};

//horizintal left cross over direction algorithm
//-----------------------------------------------
//  bound   |   value that will be returned only if (p) lies on the bound or vertex
int InsidePolygon(Point* polygon, int N, Point p, int bound)
{
    //cross points count of x
    int __count = 0;

    //neighbour bound vertices
    Point p1, p2;

    //left vertex
    p1 = polygon[0];

    //check all rays
    for(int i = 1; i <= N; ++i)
    {
        //point is an vertex
        if(p == p1) return bound;

        //right vertex
        p2 = polygon[i % N];

        //ray is outside of our interests
        if(p.y < MIN(p1.y, p2.y) || p.y > MAX(p1.y, p2.y))
        {
            //next ray left point
            p1 = p2; continue;
        }

        //ray is crossing over by the algorithm (common part of)
        if(p.y > MIN(p1.y, p2.y) && p.y < MAX(p1.y, p2.y))
        {
            //x is before of ray
            if(p.x <= MAX(p1.x, p2.x))
            {
                //overlies on a horizontal ray
                if(p1.y == p2.y && p.x >= MIN(p1.x, p2.x)) return bound;

                //ray is vertical
                if(p1.x == p2.x)
                {
                    //overlies on a ray
                    if(p1.x == p.x) return bound;
                    //before ray
                    else ++__count;
                }

                //cross point on the left side
                else
                {
                    //cross point of x
                    double xinters = (p.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x;

                    //overlies on a ray
                    if(fabs(p.x - xinters) < __DBL_EPSILON__) return bound;

                    //before ray
                    if(p.x < xinters) ++__count;
                }
            }
        }
        //special case when ray is crossing through the vertex
        else
        {
            //p crossing over p2
            if(p.y == p2.y && p.x <= p2.x)
            {
                //next vertex
                const Point& p3 = polygon[(i+1) % N];

                //p.y lies between p1.y & p3.y
                if(p.y >= MIN(p1.y, p3.y) && p.y <= MAX(p1.y, p3.y))
                {
                    ++__count;
                }
                else
                {
                    __count += 2;
                }
            }
        }

        //next ray left point
        p1 = p2;
    }

    //EVEN
    if(__count % 2 == 0) return(OUTSIDE);
    //ODD
    else return(INSIDE);
}

using namespace std;

int main()
{
Point polygon[6];

//[[320., 227.], [380., 262.], [380., 331.], [320., 366.], [260., 331.], [260., 262.]]

polygon[0].x = 320;
polygon[0].y = 227;

polygon[1].x = 380;
polygon[1].y = 262;

polygon[2].x = 380;
polygon[2].y = 331;

polygon[3].x = 320;
polygon[3].y = 366;

polygon[4].x = 260;
polygon[4].y = 331;

polygon[5].x = 260;
polygon[5].y = 262;

Point point;

cout << "ONE!" << endl;
point.x = 57;
point.y = 317;

int x = InsidePolygon(polygon, 6, point, 4);
cout << x << endl;
if (x == 1){ cout << "OK" << endl; }else{ cout << "NOT" << endl; };
cout << endl;


cout << "TWO!" << endl;
point.x = 320;
point.y = 316;

x = InsidePolygon(polygon, 6, point, 4);
cout << x << endl;
if (x == 1){ cout << "OK" << endl; }else{ cout << "NOT" << endl; };
cout << endl;


cout << "THREE!" << endl;
point.x = 320;
point.y = 227;

x = InsidePolygon(polygon, 6, point, 4);
cout << x << endl;
if (x == 1){ cout << "OK" << endl; }else{ cout << "NOT" << endl; };
cout << endl;


cout << "FOUR!" << endl;
point.x = 320;
point.y = 226;

x = InsidePolygon(polygon, 6, point, 4);
cout << x << endl;
if (x == 1){ cout << "OK" << endl; }else{ cout << "NOT" << endl; };
cout << endl;

}

