select venue_id,road_id,checkins_count, weight from (
		select venue_id, checkins_count, ((checkins_count)/(SELECT SUM(checkins_count)
		FROM open.nyc_fs_venue_join)*100) AS weight from open.nyc_fs_venue_join where st_dwithin( (
			select geom from open.nyc_road_proj_final where gid=7) ,ftus_coord, 80)
			and not st_dwithin( (
			select geom from open.nyc_road_proj_final where gid=2) ,ftus_coord, 8000))
			as fs left join open.nyc_road2fs_80ft r2f on r2f.location_id=fs.venue_id 
			where not road_id is null order by checkins_count



#test 2 where checkins sum is only for the ones within radius

select venue_id,road_id,checkins_count, weight from (
		select venue_id, checkins_count, ((checkins_count)/(SELECT SUM(checkins_count)
		FROM open.nyc_fs_venue_join
		where st_dwithin( (
			select geom from open.nyc_road_proj_final where gid=7) ,ftus_coord, 200)
			and not st_dwithin( (
			select geom from open.nyc_road_proj_final where gid=7) ,ftus_coord, 80))
		) AS weight from open.nyc_fs_venue_join where st_dwithin( (
			select geom from open.nyc_road_proj_final where gid=7) ,ftus_coord, 200)
			and not st_dwithin( (
			select geom from open.nyc_road_proj_final where gid=7) ,ftus_coord, 80))
			as fs left join open.nyc_road2fs_80ft r2f on r2f.location_id=fs.venue_id 
			where not road_id is null order by checkins_count



SELECT (checkins_count)+checkins_count AS "test1"
FROM open.nyc_fs_venue_join

SELECT SUM(checkins_count) as "sum"
FROM open.nyc_fs_venue_join


SELECT venue_id, checkins_count, (checkins_count)/(SELECT SUM(checkins_count)
FROM open.nyc_fs_venue_join)
AS weight
FROM open.nyc_fs_venue_join


SELECT COUNT(venue_id)as total_venues, SUM(checkins_count) as total_checkins
FROM open.nyc_fs_venue_join
where st_dwithin((select geom from open.nyc_road_proj_final where gid=7) ,ftus_coord, 200)
and not st_dwithin((select geom from open.nyc_road_proj_final where gid=7) ,ftus_coord, 80)

SELECT venue_id,road_id,weighted_checkins from (
SELECT venue_id, checkins_count,(checkins_count * 100.0)/temp.total_checkins as weighted_checkins
from(
SELECT COUNT(venue_id)as total_venues, SUM(checkins_count) as total_checkins
FROM open.nyc_fs_venue_join
where st_dwithin((select geom from open.nyc_road_proj_final where gid=7) ,ftus_coord, 200)
and not st_dwithin((select geom from open.nyc_road_proj_final where gid=7) ,ftus_coord, 80)
) as temp, open.nyc_fs_venue_join
where st_dwithin((select geom from open.nyc_road_proj_final where gid=7) ,ftus_coord, 200)
and not st_dwithin((select geom from open.nyc_road_proj_final where gid=7) ,ftus_coord, 80))
as fs left join open.nyc_road2fs_80ft r2f on r2f.location_id=fs.venue_id where not road_id is null

order by checkins_count
order by weighted_checkins desc

SELECT road_id, venue_id FROM (SELECT venue_id FROM open.nyc_fs_venue_join WHERE venue_id=2689445)
AS fs LEFT JOIN open.nyc_road2fs_80ft r2f ON r2f.location_id=fs.venue_id

SELECT road_id, venue_id FROM open.nyc_fs_venue_join
AS fs LEFT JOIN open.nyc_road2fs_80ft r2f ON r2f.location_id=fs.venue_id 
order by road_id desc





select venue_id,road_id,checkins_count, weight from (
		select venue_id, checkins_count, ((checkins_count)/(SELECT SUM(checkins_count)
		FROM open.nyc_fs_venue_join)*100) AS weight from open.nyc_fs_venue_join)
			as fs left join open.nyc_road2fs_80ft r2f on r2f.location_id=fs.venue_id 
			where road_id is null order by checkins_count




Select venue_id, road_id, checkins_count, weighted_checkins FROM(SELECT venue_id, checkins_count,(checkins_count * 100.0)/temp.total_checkins as weighted_checkins
                    from (SELECT COUNT(venue_id)as total_venues, SUM(checkins_count) as total_checkins FROM open.nyc_fs_venue_join
                    where st_dwithin((select geom from open.nyc_road_proj_final where gid=7),ftus_coord, 200)
                    and not st_dwithin((select geom from open.nyc_road_proj_final where gid=7),ftus_coord, 80)
                    ) as temp, open.nyc_fs_venue_join
                    where st_dwithin((select geom from open.nyc_road_proj_final where gid=7),ftus_coord, 200)
                    and not st_dwithin((select geom from open.nyc_road_proj_final where gid=7),ftus_coord, 80))
                    as fs left join open.nyc_road2fs_80ft r2f on r2f.location_id=fs.venue_id 
			where not road_id is null
