// SPDX-License-Identifier: GPL-3.0-only
// Read the actual exported package using the pinned engine's own map reader.
use skate_data::skate_map::SkateMap;
fn support(map: &SkateMap, x:f32, z:f32, max_y:f32) -> Option<f32> {
    let mut best:Option<f32>=None;
    for tri in &map.geometry.collision {
        let [a,b,c]=tri.points;
        let det=(b[2]-c[2])*(a[0]-c[0])+(c[0]-b[0])*(a[2]-c[2]);
        if det.abs()<1e-9 {continue;}
        let u=((b[2]-c[2])*(x-c[0])+(c[0]-b[0])*(z-c[2]))/det;
        let v=((c[2]-a[2])*(x-c[0])+(a[0]-c[0])*(z-c[2]))/det;
        let w=1.-u-v;
        if u< -1e-5 || v< -1e-5 || w< -1e-5 {continue;}
        let y=u*a[1]+v*b[1]+w*c[1];
        // Only upward faces provide standing support.
        let ny=(b[2]-a[2])*(c[0]-a[0])-(b[0]-a[0])*(c[2]-a[2]);
        if ny>0. && y<=max_y && best.is_none_or(|old|y>old) {best=Some(y);}
    }
    best
}
fn main()->Result<(),String>{
    let path=std::env::args_os().nth(1).ok_or("Usage: skate_map_probe MAP.skate")?;
    let map=SkateMap::load(std::path::Path::new(&path))?;
    let offsets=std::env::args().skip(2).map(|v|v.parse::<f32>().expect("Offsets must be metres")).collect::<Vec<_>>();
    assert!(offsets.is_empty()||offsets.len()==2,"Pass both X and Z offsets");
    let [offset_x,offset_z]=if offsets.is_empty(){[0.,0.]}else{[offsets[0],offsets[1]]};
    // Mirror the runtime's 1 mm global weld, then use its real volume constructor.
    let mut weld=std::collections::HashMap::<[i64;3],usize>::new();
    let mut positions=Vec::<[f32;3]>::new();
    let mut invalid=Vec::new();
    for (index,tri) in map.geometry.collision.iter().enumerate(){
        let material=&map.materials[(tri.material-1) as usize];
        assert_eq!(tri.surface,material.audio | (material.physics<<7) | (material.pattern<<12),"Collision {index}: packed contact tag does not match material");
        let category=(tri.surface>>7)&31;
        assert!(category<16,"Collision {index}: invalid physics category {category}");
        let chosen=skate_core::physics::contact_feedback::choose_surface([category;4],[true;4],false);
        assert_eq!(chosen,category,"Collision {index}: contact feedback classification mismatch");
        let points=tri.points.map(|p|{
            let key=p.map(|v|(f64::from(v)/f64::from(0.001_f32)).round() as i64);
            let id=*weld.entry(key).or_insert_with(||{let id=positions.len();positions.push(p);id});
            positions[id]
        });
        let v=points.map(|p|skate_core::math::Vector3::new(p[0],p[1],p[2]));
        let contact=skate_core::physics::contact::RetailContactMaterial{static_friction:0.82,dynamic_friction:0.82,restitution:0.};
        if skate_core::physics::board_world::WorldTriangle::from_vertices(v,contact,tri.surface,0,[1.;3],0.).is_none(){invalid.push(serde_json::json!({"index":index,"points":tri.points,"after_1mm_weld":points}));}
    }
    if !invalid.is_empty(){
        println!("{}",serde_json::to_string_pretty(&serde_json::json!({"status":"invalid_runtime_collision_volumes","invalid":invalid})).unwrap());
        return Err("Some collision triangles collapse under the runtime's 1 mm weld".into());
    }
    let scale=1.0640686466_f32;
    assert_eq!(map.rails.len(),4,"Expected four authored grind paths");
    assert!(map.geometry.indices.len()>10000 && map.geometry.collision.len()>1000);
    for rail in &map.rails {assert!(rail.points.len()>=2);}
    let floor=support(&map,map.spawn[0],map.spawn[2],map.spawn[1]).ok_or("Spawn unsupported")?;
    assert!((floor+0.08/scale).abs()<0.08,"Unexpected spawn support {floor}");
    assert!(map.spawn[1]-floor>0.15 && map.spawn[1]-floor<0.4);
    let checks=[("kicker",-4.0,-7.8,0.25,0.65),("manual island",33.,-7.6,0.20,0.45),("curved return",51.,-7.15,0.65,1.7),("ledge",-16.,-9.1,0.3,0.6),("flatbar",15.6,-7.8,0.5,0.8)];
    let mut samples=Vec::new();
    for (name,x,y,lo,hi) in checks {
        let top=support(&map,x/scale-offset_x,-y/scale-offset_z,2.0).ok_or(format!("Missing {name} collision"))?;
        assert!(top>=lo && top<=hi,"{name}: height {top} outside {lo}..{hi}");
        samples.push(serde_json::json!({"feature":name,"collision_top_metres":top}));
    }
    let mut run_out=Vec::new();
    for x in [-23.,-10.,0.,8.,23.,40.,47.] {
        let top=support(&map,x/scale-offset_x,5.3/scale-offset_z,1.0).ok_or("Run-out floor missing")?;
        assert!(top.abs()<0.2,"Run-out unexpectedly raised at {x}: {top}");
        run_out.push(serde_json::json!({"x_BU":x,"support_metres":top}));
    }
    println!("{}",serde_json::to_string_pretty(&serde_json::json!({"map":map.name,"version":map.version,"visual_triangles":map.geometry.indices.len()/3,"collision_triangles":map.geometry.collision.len(),"textures":map.textures.len(),"rails":map.rails.len(),"spawn":map.spawn,"spawn_support_metres":floor,"features":samples,"run_out_floor_samples":run_out,"status":"map_reader_and_selected_collision_samples_pass","limits":"Static package checks only; not skating, animation, trick, grind or runtime rendering validation."})).unwrap());
    Ok(())
}
