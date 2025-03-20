!===================================================================================================================================
! Copyright (c) 2025 GVEC Contributors, Max Planck Institute for Plasma Physics
! License: MIT
!===================================================================================================================================

!===================================================================================================================================
!>
!!# Module ** Read State Variables **
!!
!!
!!
!===================================================================================================================================
MODULE MODgvec_ReadState_Vars
! MODULES
USE MODgvec_Globals,ONLY:wp
USE MODgvec_sgrid,  ONLY: t_sgrid
USE MODgvec_base,   ONLY: t_base
USE MODgvec_sbase,  ONLY: t_sbase
USE MODgvec_c_hmap, ONLY: c_hmap
IMPLICIT NONE
PUBLIC
!-----------------------------------------------------------------------------------------------------------------------------------
! GLOBAL VARIABLES 
  INTEGER                   :: fileID_r,OutputLevel_r
  CLASS(c_hmap),ALLOCATABLE :: hmap_r                 !! container for global coordinate system
  TYPE(t_sgrid)             :: sgrid_r                !! container for the grid of X1,X2,LA
  CLASS(t_sbase),ALLOCATABLE:: sbase_prof             !! container for base for profiles
  CLASS(t_base),ALLOCATABLE :: X1_base_r              !! container for base of X1
  CLASS(t_base),ALLOCATABLE :: X2_base_r              !! container for base of X2
  CLASS(t_base),ALLOCATABLE :: LA_base_r              !! container for base of LA
  REAL(wp),ALLOCATABLE      :: X1_r(:,:)              !! spline x fourier coefs of solution X1
  REAL(wp),ALLOCATABLE      :: X2_r(:,:)              !! spline x fourier coefs of solution X2
  REAL(wp),ALLOCATABLE      :: LA_r(:,:)              !! spline x fourier coefs of solution LA 
  REAL(wp),ALLOCATABLE      :: profiles_1d(:,:)       !! spline coefficients for 1d profiles (using X1_base...needs to be improved!)
  REAL(wp)                  :: a_minor,r_major,volume !! scalars: average minor and major radius, total volume
!===================================================================================================================================
END MODULE MODgvec_ReadState_Vars

