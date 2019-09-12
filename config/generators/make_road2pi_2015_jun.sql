select object_id, road_id, offense, off_type, distance into open.nyc_road2pi_5ft from (
SELECT g1.objectid As object_id, g1.offense as offense, 0 as off_type, g2.gid As road_id, ST_Distance(g1.ftus_coord,g2.geom) as distance, g1.ftus_coord,g2.geom
 FROM open.nyc_police_incident As g1, open.nyc_road_proj_final As g2 
 WHERE ST_DWithin(g1.ftus_coord, g2.geom, 5) and occurence_year=2015 and occurrence_month='Jun'
 ) as foo
;
commit;
alter table open.nyc_road2pi_5ft owner to shared_open;
commit;