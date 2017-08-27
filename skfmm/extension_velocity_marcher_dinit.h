//extension_velocity_marcher_dinit.h
#pragma once

#include "extension_velocity_marcher.h"

class extensionVelocityMarcherDInit : public extensionVelocityMarcher
{
  public:
    extensionVelocityMarcherDInit(double *phi,      double *dx,    long *flag,
                           double *distance, int     ndim,  int *shape,
                           bool self_test,   int order,     long *ext_mask,
                           double *speed,
                           double *f_ext,    double narrow, int periodic,
                           double *dinit, double *finit) :
        extensionVelocityMarcher(phi, dx, flag, distance, ndim, shape, self_test,
                    order, ext_mask, speed, f_ext, narrow, periodic),
        dinit_(dinit), finit_(finit) {}

    virtual ~extensionVelocityMarcherDInit() { }

    virtual void initalizeFrozen();

  private:
    double * dinit_;
    double * finit_;
};
