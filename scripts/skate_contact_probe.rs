// SPDX-License-Identifier: GPL-3.0-only
// Exercise real map face contacts through the production wheel query and solver.
// This is a contact stress check, not the full controller/animation simulation.
use skate_data::skate_map::SkateMap;
use skate_core::{math::Vector3,physics::{
    board::RETAIL_WHEEL_RADIUS,
    board_world::WorldTriangle,
    collision::{Sphere,TriangleFeature,WorldContactSettings,sphere_triangle_world_contact},
    contact::{RetailContactBodyState,RetailContactInput,RetailContactMaterial,generate_contact},
    contact_solver::build_contact_jacobian,
    mass::retail_wheel_mass_properties,
    rigid_body::RetailReactionCorrections,
    solver::solve_constraints,
}};
fn finite(v:Vector3)->bool{v.x.is_finite()&&v.y.is_finite()&&v.z.is_finite()}
fn add(a:Vector3,b:Vector3)->Vector3{Vector3::new(a.x+b.x,a.y+b.y,a.z+b.z)}
fn scale(a:Vector3,s:f32)->Vector3{Vector3::new(a.x*s,a.y*s,a.z*s)}
fn dot(a:Vector3,b:Vector3)->f32{a.x*b.x+a.y*b.y+a.z*b.z}
fn main()->Result<(),String>{
    let path=std::env::args_os().nth(1).ok_or("Usage: pharmacie_contact_probe MAP.skate")?;
    let map=SkateMap::load(std::path::Path::new(&path))?;
    let inertia=retail_wheel_mass_properties().dynamics;
    let mut cases=0;let mut faces=0;let mut names=std::collections::BTreeSet::new();
    let mut maximum_reaction=0_f32;
    for (index,tri) in map.geometry.collision.iter().enumerate(){
        let mat=&map.materials[(tri.material-1) as usize];
        // Authored banks, return ramp, island, ledge and rail components.
        if !mat.name.contains("Skate v60 |"){continue;}
        let vertices=tri.points.map(|p|Vector3::new(p[0],p[1],p[2]));
        let world=WorldTriangle::from_vertices(vertices,RetailContactMaterial{
            static_friction:mat.friction,dynamic_friction:mat.friction,restitution:mat.restitution,
        },tri.surface,TriangleFeature::ONE_SIDED,[1.;3],0.).ok_or("Invalid feature triangle")?;
        let normal=world.triangle.feature.normal;
        if normal.y<0.05{continue;}
        assert_eq!(tri.surface,mat.audio|(mat.physics<<7)|(mat.pattern<<12));
        assert!(mat.physics<14);
        let center=add(scale(add(add(vertices[0],vertices[1]),vertices[2]),1./3.),scale(normal,RETAIL_WHEEL_RADIUS-0.001));
        let raw_tangent=add(Vector3::new(1.,0.,0.),scale(normal,-normal.x));
        let tangent=scale(raw_tangent,1./dot(raw_tangent,raw_tangent).sqrt());
        names.insert(mat.name.clone());faces+=1;
        for speed in [0.,3.,8.,15.] {for descent in [0.,2.,5.] {
            let velocity=add(scale(tangent,speed),scale(normal,-descent));
            let pair=sphere_triangle_world_contact(Sphere{center,radius:RETAIL_WHEEL_RADIUS},world.triangle,velocity,
                WorldContactSettings{volume_padding:0.,maximum_separating_distance:0.,edge_cos_bend_normal_threshold:-1.,convexity_epsilon:0.,is_object:false})
                .ok_or(format!("Feature face {index}: missing wheel contact at speed {speed}, descent {descent}"))?;
            assert!(finite(pair.normal)&&finite(pair.points.a)&&finite(pair.points.b));
            let static_body=RetailContactBodyState{
                contact_body_id:u32::MAX,reaction_id:1,state:0,center_of_mass:Vector3::ZERO,
                inverse_inertia_full:Vector3::ZERO,inverse_inertia_split:Vector3::ZERO,inverse_mass:0.,
                force_acceleration:Vector3::ZERO,torque_acceleration:Vector3::ZERO,
                linear_velocity:Vector3::ZERO,angular_velocity:Vector3::ZERO,kinetic_energy:0.,cool_down:0,
            };
            let wheel=RetailContactBodyState{contact_body_id:0,reaction_id:0,state:4,center_of_mass:center,
                inverse_inertia_full:Vector3::new(inertia.inverse_tensor.x,0.,0.),
                inverse_inertia_split:Vector3::new(inertia.inverse_tensor.z,inertia.inverse_tensor.y,0.),
                inverse_mass:inertia.inverse_mass,force_acceleration:Vector3::new(0.,-9.8,0.),
                linear_velocity:velocity,..static_body};
            let mut contacts=[build_contact_jacobian(generate_contact(RetailContactInput{
                position_on_a:pair.points.a,position_on_b:pair.points.b,normal:pair.normal,
                static_friction:mat.friction,dynamic_friction:mat.friction,restitution:mat.restitution,tag:tri.surface,
            },wheel,static_body),1./60.)];
            let mut reactions=[RetailReactionCorrections::default();2];
            solve_constraints(&mut contacts,&mut [],&mut [],&mut reactions,25);
            assert_eq!(reactions[1],RetailReactionCorrections::default(),"Static map moved");
            assert!(finite(reactions[0].linear_displacement)&&finite(reactions[0].angular_displacement),"Nonfinite reaction at face {index}");
            maximum_reaction=maximum_reaction.max(dot(reactions[0].linear_displacement,reactions[0].linear_displacement).sqrt());
            assert_eq!(skate_core::physics::contact_feedback::choose_surface([mat.physics;4],[true;4],false),mat.physics);
            cases+=1;
        }}
    }
    assert!(faces>50&&cases>600,"Too few authored feature contacts tested");
    println!("{}",serde_json::to_string_pretty(&serde_json::json!({
        "status":"authored_feature_face_wheel_contact_solver_pass","sampled_upward_feature_faces":faces,
        "wheel_contact_cases":cases,"tangential_speeds_mps":[0,3,8,15],"normal_descent_speeds_mps":[0,2,5],
        "solver_iterations":25,"maximum_linear_reaction_displacement_m":maximum_reaction,"materials":names,
        "limits":"Independent face-centre wheel contacts through core query/generator/solver. Does not test multi-body board dynamics, feature edges, full animation/controller runtime, transitions, tricks or ridden landings."
    })).unwrap());Ok(())
}
