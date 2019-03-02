&constants

/

&model
	model_type = 'EVOL'  ! Obtain stellar structure from an evolutionary model
	file = 'LOGS/folder/modelname_NNN.profile.GYRE'    ! File name of the evolutionary model
	file_format = 'MESA' ! File format of the evolutionary model
/

&mode
	l = 0                ! Harmonic degree
/

&osc
	outer_bound = 'VACUUM' ! Use a zero-pressure outer mechanical boundary condition
/

&num
	diff_scheme = 'COLLOC_GL4' ! 4th-order collocation scheme for difference equations
/

&scan
	grid_type = 'LINEAR' 		! Scan for modes using a uniform-in-frequency grid; best for p modes
	freq_min_units = 'UHZ'   	! Interpret freq_min as being in uHz
	freq_max_units = 'UHZ'	 	! Interpret freq_max as being in uHz
	freq_min = 10       		! Minimum frequency to scan from
	freq_max = 150       		! Maximum frequency to scan to
	n_freq = 200          		! Number of frequency points in scan
/

&grid
	alpha_osc = 10  ! Ensure at least 10 points per wavelength in propagation regions
	alpha_exp = 2   ! Ensure at least 2 points per scale length in evanescent regions
	n_inner = 5     ! Ensure at least 5 points between center and inner turning point
/


&ad_output
	freq_units = 'UHZ'	! Interpret freq_min and freq_max as having units of microHertz
	summary_file = 'LOGS/folder/modelname_NNN.summary.txt'                    ! File name for summary file
	summary_file_format = 'TXT'                             ! Format of summary file
	summary_item_list = 'M_star,R_star,l,n_pg,freq,E_norm' ! Items to appear in summary file
	!mode_template = 'LOGS/folder/modeNNN_.%J.txt'                			! File-name template for mode files
	!mode_file_format = 'TXT'                   				! Format of mode files
	!mode_item_list = 'l,n_pg,omega,x,xi_r,xi_h'				! Items to appear in mode files
/

&nad_output
/

