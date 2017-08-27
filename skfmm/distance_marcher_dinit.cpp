#include "distance_marcher_dinit.h"

void distanceMarcherDInit::initalizeFrozen()
{
  // this is a special case of the init frozen because the distance to
  // the zero contour of the initially frozen points has been pre-calculated
  // in the python wrapper.
  for (int i=0; i<size_; i++)
  {
    if (! (dinit_[i] == maxDouble))
    {
      flag_[i] = Frozen;
      distance_[i] = dinit_[i];
    }
  }

  // call the base class method for linear interpolation of those points
  // where the precalculation failed
  distanceMarcher::initalizeFrozen();
}
