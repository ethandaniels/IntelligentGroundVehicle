/* This function will create a compass reading based on: magnemoeter and gyro
values. As magnemoeter is only truly accurate when taking level readings.
Along with this magnetic deliniation will be manually updated in the code based
on general city location.

This is not optimal though deliniation would only change by ~.2º around the course

Set your calculators to raidans boys

Anytime you see *variable, this is a pointer. Must be used to pull values from other functions, it allows
to pull variables from physical memory.

Ref: https://www.ngdc.noaa.gov/geomag-web/

UPDATE: 2017.8.8. May want to implement this correction code
http://x-io.co.uk/open-source-imu-and-ahrs-algorithms/
*/

double declination = -14.25*(PI/180);

//psi is roll (z), theta is PItch (y)
double readComp(double *magX, double *magY, double *magZ, double *psi, double *theta)
{
    //converting to radians
    *magX = *magX*(PI/180);
    *magY = *magY*(PI/180);
    *magZ = *magZ*(PI/180);

    double x = *magX*cos(*theta)+*magY*sin(*psi)*sin(*theta)+*magZ*cos(*psi)-*magZ*sin(*psi);
    double y = *magY+cos(*psi)-*magZ*sin(*psi);

    double headingRad = (atan2(-y,x)+declination);
    double headingDeg = headingRad*(180/PI);

    double nearestHeadDeg = roundf(headingDeg * 100) / 100;

    return nearestHeadDeg;
}
