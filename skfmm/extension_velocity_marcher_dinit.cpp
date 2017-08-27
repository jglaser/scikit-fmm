#include "extension_velocity_marcher_dinit.h"

void extensionVelocityMarcherDInit::initalizeFrozen()
{
  int c=0;
  for (int i=0; i<size_; i++)
  {
    if (! (dinit_[i] == maxDouble) && !(finit_[i] == maxDouble))
    {
      c++;
      flag_[i] = Frozen;
      distance_[i] = dinit_[i];
      f_ext_[i] = finit_[i];
    }
  }

  // call the base class method for linear interpolation of those points
  // where the precalculation failed
  extensionVelocityMarcher::initalizeFrozen();
}
