### Additional Information on the HeII region
___

_(Notes build on content in project proposal)_


In RGB stars, the predominant source of any sound-speed discontinuity is due to the presence of He II ionisation regions, with secondary sources including the base of the convective zone (BCZ). Stars within the mass range ~0.8-1.5M-sun are most suitable for our analysis:

* Above 1.5Msun, a secondary local minimum appears in the adiabatic exponent (Γ) due to the appearance of the second helium ionisation region (He I). In addition, the location (as an acoustic diameter) of the He II zone and the BCZ become similar, leading to the intereference between the two oscillatory signals (See _Miglio et al. (2003)_).
* As the mass decreases, the amplitude of ν-max decreases (and hence the overall envelope encompassing the oscillations across the spectral frequency range). As a result the signals become too small to be able to perform useful analysis.


RGB stars within this mass range are particularly useful since the HeII zone is far from the turning points of the pressure modes (one such point being at the convective region boundary BCZ, which is ~0.1R; the other located near the surface) -- as such this region of the interior is adiabatically stratified.

The vertical wavenumber can be approximated by neglecting acoustic cut-off frequency (ω_a) and we can use the simplified asymptotic relations for the wavefunctions, eg.

	Δν = (2 int[0,R] 1/c dr)^-1


The overall amplitude of the glitch is directly related to the amount of He present in the convective envelope. The amplitude of ν-max is a use proxy with which to measure this.

_NOTE: In the paper by Broomhall et al (2014) their analysis proposes that the location of the acoustic depth of the He II region is near the local maximum in the distribution for γ1, however model and other authors suggest this should be the local minimum in fact. Potentially could be attributed to surface effects that are unaccounted for, but may be an error in their procedure?_

#### Acoustic Modes

On the whole, due to their larger size, RGB stars pulsate at lower radial orders compared to their main sequence counterparts (~10 vs ~20). The modes in the power spectrum can be located using a Lorentzian fit:

	M(ν) = H / [1 + 2(ν-νk)/Γ]^2

The additional curvature term visible in an Échelle Diagram can be modelled using the following relation

	ν(n,0) = (n + ε + α/2(n-nmax)^2)<Δν>

whilst the subsequent subtraction of this term allows the fitting of an oscillatory signal _(example see oscillationshbm.ipynb)_, which can be modelled using

	δ = A<Δν> cos[2π(ν-νmax)/G<Δν>  + φ]

> Explanation of equation terms to be added.


### Notes from Casegrande et al. (2008)

As previously discussed in project proposal, the He content of low mass stars cannot be measured by direct means. Typically, one of the techniques used is to measure the differential production of Y relative to Z (ie ΔΥ/ΔΖ) ~ 2.1+-0.4. This ratio can be extrapolated back to find the primordial abundance Y_p.

It is often assumed however that this ratio is constant and stars can be scaled from the solar value using 

	Y = Ysun + ΔΥ/ΔΖ * (Z-Zsun)

however, recent studies are beginning to show that is not quite accurate. Examples are being found of clusters that both conform and break this rule, one example being the Hyades, which is deficient in Y for the measured metal content. Other cluster such as  ω Cen have even been observed with with multiple MS turn-off populations, suggesting populations with different abundance ratios. Together, this tends to support the notion that there may be some natural spread in the chemical evolution throughout difference regions of our galaxy. This is additionally backed up by the fact that Helium can be introduced into the  interstellar medium via more localised processes, such as thermally pulsing AGB stars and Type 1a supernovae.

