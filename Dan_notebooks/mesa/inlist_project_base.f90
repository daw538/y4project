! inlist to evolve a 1 solar mass star with axion cooling options

! For the sake of future readers of this file (yourself included),
! ONLY include the controls you are actually using.  DO NOT include
! all of the other controls that simply have their default values.

&star_job

  ! begin with a pre-main sequence model
    create_pre_main_sequence_model = .true.
    pre_ms_T_c = 6d5

  ! display on-screen plots
    pgstar_flag = .true.

/ !end of star_job namelist


&controls

  ! Log file names - please change appropriately
    star_history_name   = 'Mxxx_Yzzz_mmdd.data'  ! M<mass>_<info>_<date>.data
    profiles_index_name = 'Mxxx_Yzzz_mmdd.index' ! M<mass>_<info>_<date>.index
    profile_data_prefix = 'Mxxx_Yzzz_mmdd_'      ! M<mass>_<info>_<date>_
    profile_data_suffix = '.profile' ! Don't change this

    initial_mass = xxx ! in Msun units
    initial_y = zzzd0 ! initial He composition
  !note rgb bump appears to occur around model 1800-1900

  ! GYRE implementation
    write_pulse_data_with_profile = .true.
    pulse_data_format = 'GYRE'

  ! stopping conditions:
    log_center_temp_limit = 7.6
  !  xa_central_lower_limit_species(1) = 'h1'
  !  xa_central_lower_limit(1) = 1d-3

  ! file intervals and limits
    log_directory = 'LOGS/folder'
    terminal_interval = 5
    history_interval = 5
    profile_interval = 0
    photo_interval = 100
    max_num_profile_models = 1000


/ ! end of controls namelist
