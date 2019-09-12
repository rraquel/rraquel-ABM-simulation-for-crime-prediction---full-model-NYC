-- 2301 is max(population_density)/100 
-- Runs only on postgres 9.5+
UPDATE open.nyc_pluto_areas pl SET (census_population_weight) =
    (SELECT round(population_density/2301) from open.nyc_census_tract_features cf where 
    st_isvalid(pl.geom) and 
    st_within(pl.geom,cf.geom_ftus)
    );
commit;

-- select gid,st_distance(st_centroid(g1.geom),g2.geom_ftus) from open.nyc_pluto_areas g1, open.nyc_census_tract_features g2
--  where census_population_weight=0 and st_dwithin(st_centroid(g1.geom),g2.geom_ftus,300);
