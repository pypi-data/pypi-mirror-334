!===================================================================================================================================
! Copyright (c) 2025 GVEC Contributors, Max Planck Institute for Plasma Physics
! License: MIT
!===================================================================================================================================
#include "defines.h"

!===================================================================================================================================
!>
!!# Module ** c_hmap **
!!
!! contains only the abstract type to point to a specific map h (maps  omega_p x S^1 --> omega) 
!!
!===================================================================================================================================
MODULE MODgvec_c_hmap
! MODULES
USE MODgvec_Globals    ,ONLY:wp,Unit_stdOut,abort
IMPLICIT NONE

PUBLIC
!-----------------------------------------------------------------------------------------------------------------------------------
! TYPES 
!-----------------------------------------------------------------------------------------------------------------------------------
TYPE, ABSTRACT :: c_hmap
  !---------------------------------------------------------------------------------------------------------------------------------
  !input parameters
  INTEGER              :: which_hmap         !! points to hmap (1: MHD3D) 
  INTEGER              :: nfp=-1             !! number of field periods used in hmap. If =-1, its not used
  !---------------------------------------------------------------------------------------------------------------------------------
  CONTAINS
    PROCEDURE(i_sub_hmap            ),DEFERRED :: init
    PROCEDURE(i_sub_hmap            ),DEFERRED :: free
    PROCEDURE(i_fun_hmap_eval       ),DEFERRED :: eval
    !PROCEDURE(i_fun_hmap_eval_all   ),DEFERRED :: eval_all
    PROCEDURE(i_sub_hmap_init_aux   ),DEFERRED :: init_aux
    PROCEDURE(i_sub_hmap            ),DEFERRED :: free_aux
    PROCEDURE(i_sub_hmap            ),DEFERRED :: eval_aux
    PROCEDURE(i_fun_hmap_eval_dxdq  ),DEFERRED :: eval_dxdq
    PROCEDURE(i_fun_hmap_eval_Jh    ),DEFERRED :: eval_Jh    
    PROCEDURE(i_fun_hmap_eval_Jh_dq ),DEFERRED :: eval_Jh_dq1 
    PROCEDURE(i_fun_hmap_eval_Jh_dq ),DEFERRED :: eval_Jh_dq2 
    PROCEDURE(i_fun_hmap_eval_gij   ),DEFERRED :: eval_gij   
    PROCEDURE(i_fun_hmap_eval_gij_dq),DEFERRED :: eval_gij_dq1
    PROCEDURE(i_fun_hmap_eval_gij_dq),DEFERRED :: eval_gij_dq2
  !---------------------------------------------------------------------------------------------------------------------------------
END TYPE c_hmap

ABSTRACT INTERFACE
  SUBROUTINE i_sub_hmap( sf )
    IMPORT c_hmap
    CLASS(c_hmap), INTENT(INOUT) :: sf
  END SUBROUTINE i_sub_hmap


  SUBROUTINE i_sub_hmap_init_aux( sf ,nzeta_aux,zeta_aux)
    IMPORT c_hmap,wp
    INTEGER,INTENT(IN)   :: nzeta_aux
    REAL(wp),INTENT(IN)  :: zeta_aux(1:nzeta_aux)
    CLASS(c_hmap), INTENT(INOUT) :: sf
  END SUBROUTINE i_sub_hmap_init_aux

  !===============================================================================================================================
  !> evaluate the mapping h q=(X^1,X^2,zeta) -> (x,y,z) 
  !!
  !===============================================================================================================================
  FUNCTION i_fun_hmap_eval( sf ,q_in) RESULT(x_out)
    IMPORT wp,c_hmap
    CLASS(c_hmap), INTENT(INOUT) :: sf
    REAL(wp)     , INTENT(IN   ) :: q_in(3)
    REAL(wp)                     :: x_out(3)
  END FUNCTION i_fun_hmap_eval
  
  !===============================================================================================================================
  !> evaluate total derivative of the mapping  sum k=1,3 (dx(1:3)/dq^k) q_vec^k,
  !! where dx(1:3)/dq^k, k=1,2,3 is evaluated at q_in=(X^1,X^2,zeta) ,
  !!
  !===============================================================================================================================
  FUNCTION i_fun_hmap_eval_dxdq( sf ,q_in,q_vec) RESULT(dxdq_qvec)
    IMPORT wp,c_hmap
    CLASS(c_hmap), INTENT(INOUT) :: sf
    REAL(wp)     , INTENT(IN   ) :: q_in(3)
    REAL(wp)     , INTENT(IN   ) :: q_vec(3)
    REAL(wp)                     :: dxdq_qvec(3)
  END FUNCTION i_fun_hmap_eval_dxdq
  
  !===============================================================================================================================
  !> evaluate Jacobian of mapping h: J_h=sqrt(det(G)) at q=(X^1,X^2,zeta)
  !!
  !===============================================================================================================================
  FUNCTION i_fun_hmap_eval_Jh( sf ,q_in) RESULT(Jh)
    IMPORT wp,c_hmap
    CLASS(c_hmap), INTENT(INOUT) :: sf
    REAL(wp)     , INTENT(IN   ) :: q_in(3)
    REAL(wp)                     :: Jh
  END FUNCTION i_fun_hmap_eval_Jh
  
  !===============================================================================================================================
  !> evaluate derivative of Jacobian of mapping h: dJ_h/dq^k, k=1,2 at q=(X^1,X^2,zeta) 
  !!
  !===============================================================================================================================
  FUNCTION i_fun_hmap_eval_Jh_dq( sf ,q_in) RESULT(Jh_dq)
    IMPORT wp,c_hmap
    CLASS(c_hmap), INTENT(INOUT) :: sf
    REAL(wp)     , INTENT(IN   ) :: q_in(3)
    REAL(wp)                     :: Jh_dq
  END FUNCTION i_fun_hmap_eval_Jh_dq
  
  !===============================================================================================================================
  !>  evaluate sum_ij (qL_i (G_ij(q_G)) qR_j) ,
  !! where qL=(dX^1/dalpha,dX^2/dalpha ,dzeta/dalpha) and qR=(dX^1/dbeta,dX^2/dbeta ,dzeta/dbeta) and 
  !! dzeta_dalpha then known to be either 0 of ds and dtheta and 1 for dzeta
  !!
  !===============================================================================================================================
  FUNCTION i_fun_hmap_eval_gij( sf ,qL_in,q_G,qR_in) RESULT(g_ab)
    IMPORT wp,c_hmap
    CLASS(c_hmap), INTENT(INOUT) :: sf
    REAL(wp)     , INTENT(IN   ) :: qL_in(3)
    REAL(wp)     , INTENT(IN   ) :: q_G(3)
    REAL(wp)     , INTENT(IN   ) :: qR_in(3)
    REAL(wp)                     :: g_ab
  END FUNCTION i_fun_hmap_eval_gij
  
  !===============================================================================================================================
  !>  evaluate sum_ij (qL_i d/dq^k(G_ij(q_G)) qR_j) , k=1,2
  !! where qL=(dX^1/dalpha,dX^2/dalpha ,dzeta/dalpha) and qR=(dX^1/dbeta,dX^2/dbeta ,dzeta/dbeta) and 
  !! dzeta_dalpha then known to be either 0 of ds and dtheta and 1 for dzeta
  !!
  !===============================================================================================================================
  FUNCTION i_fun_hmap_eval_gij_dq( sf,qL_in,q_G,qR_in) RESULT(g_ab_dq)
    IMPORT wp,c_hmap
    CLASS(c_hmap), INTENT(INOUT) :: sf
    REAL(wp)     , INTENT(IN   ) :: qL_in(3)
    REAL(wp)     , INTENT(IN   ) :: q_G(3)
    REAL(wp)     , INTENT(IN   ) :: qR_in(3)
    REAL(wp)                     :: g_ab_dq
  END FUNCTION i_fun_hmap_eval_gij_dq
  
END INTERFACE

!===================================================================================================================================



END MODULE MODgvec_c_hmap

