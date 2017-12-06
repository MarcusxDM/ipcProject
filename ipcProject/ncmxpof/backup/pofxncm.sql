SELECT pof.cod, pof.descript, ncm.cod, ncm.descript
  FROM public.ncmxpof_pof as pof, public.ncmxpof_ncm as ncm
	WHERE pof.id = ncm.pof_id;
