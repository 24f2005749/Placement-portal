import { createRouter, createWebHistory } from "vue-router"

import Login from "@/pages/auth/Login.vue"
import Register from "@/pages/auth/Register.vue"
import CompleteProfile from "@/pages/auth/CompleteProfile.vue"
import Landing from "@/pages/Landing.vue"

import StudentDashboard from "@/pages/student/Dashboard.vue"
import StudentDrives from "@/pages/student/Drives.vue"
import StudentCompanies from "@/pages/student/Companies.vue"
import StudentDriveDetails from "@/pages/student/DriveDetails.vue"
import StudentApplications from "@/pages/student/Applications.vue"
import StudentProfile from "@/pages/student/Profile.vue"

import CompanyDashboard from "@/pages/company/Dashboard.vue"
import CompanyProfile from "@/pages/company/Profile.vue"
import CompanyDrives from "@/pages/company/Drives.vue"
import CompanyCreateDrive from "@/pages/company/CreateDrive.vue"
import CompanyEditDrive from "@/pages/company/EditDrive.vue"
import CompanyDriveDetails from "@/pages/company/DriveDetails.vue"
import Applicants from "@/pages/company/Applicants.vue"

import AdminDashboard from "@/pages/admin/Dashboard.vue"
import AdminCompanies from "@/pages/admin/Companies.vue"
import AdminDriveApproval from "@/pages/admin/DriveApproval.vue"
import AdminBranches from "@/pages/admin/Branches.vue"
import AdminStudents from "@/pages/admin/Students.vue"
import AdminApplications from "@/pages/admin/Applications.vue"

const routes = [

    {
        path:"/",
        component:Landing
    },

    {
        path:"/login",
        component:Login
    },

    {
        path:"/register",
        component:Register
    },

    {
        path:"/complete-profile",
        component:CompleteProfile,
        meta:{requiresAuth:true,allowIncomplete:true}
    },

    {
        path:"/student/dashboard",
        component:StudentDashboard,
        meta:{requiresAuth:true,role:"student"}
    },

    {
        path:"/student/drives",
        component:StudentDrives,
        meta:{requiresAuth:true,role:"student"}
    },

    {
        path:"/student/companies",
        component:StudentCompanies,
        meta:{requiresAuth:true,role:"student"}
    },

    {
        path:"/student/drives/:id",
        component:StudentDriveDetails,
        meta:{requiresAuth:true,role:"student"}
    },

    {
        path:"/student/applications",
        component:StudentApplications,
        meta:{requiresAuth:true,role:"student"}
    },

    {
        path:"/student/profile",
        component:StudentProfile,
        meta:{requiresAuth:true,role:"student"}
    },


    {
        path:"/company/dashboard",
        component:CompanyDashboard,
        meta:{requiresAuth:true,role:"company"}
    },

    {
        path:"/company/profile",
        component:CompanyProfile,
        meta:{requiresAuth:true,role:"company"}
    },

    {
        path:"/company/drives",
        component:CompanyDrives,
        meta:{requiresAuth:true,role:"company"}
    },

    {
        path:"/company/drives/create",
        component:CompanyCreateDrive,
        meta:{requiresAuth:true,role:"company"}
    },

    {
        path:"/company/drives/:id/edit",
        component:CompanyEditDrive,
        meta:{requiresAuth:true,role:"company"}
    },

    {
        path:"/company/drives/:id",
        component:CompanyDriveDetails,
        meta:{requiresAuth:true,role:"company"}
    },

    {
        path:"/company/drives/:id/applicants",
        component:Applicants,
        meta:{requiresAuth:true,role:"company"}
    },


    {
        path:"/admin/dashboard",
        component:AdminDashboard,
        meta:{requiresAuth:true,role:"admin"}
    },

    {
        path:"/admin/companies",
        component:AdminCompanies,
        meta:{requiresAuth:true,role:"admin"}
    },

    {
        path:"/admin/company-approval",
        redirect:"/admin/companies"
    },

    {
        path:"/admin/drives",
        component:AdminDriveApproval,
        meta:{requiresAuth:true,role:"admin"}
    },

    {
        path:"/admin/drive-approval",
        redirect:"/admin/drives"
    },

    {
        path:"/admin/branches",
        component:AdminBranches,
        meta:{requiresAuth:true,role:"admin"}
    },

    {
        path:"/admin/students",
        component:AdminStudents,
        meta:{requiresAuth:true,role:"admin"}
    },

    {
        path:"/admin/applications",
        component:AdminApplications,
        meta:{requiresAuth:true,role:"admin"}
    },

    {
        path:"/admin/search",
        redirect:"/admin/companies"
    },

    {
        path:"/:pathMatch(.*)*",
        redirect:"/login"
    }

]

const router = createRouter({

    history:createWebHistory(),

    routes

})

router.beforeEach((to)=>{

    const token = localStorage.getItem("token")

    const user = JSON.parse(localStorage.getItem("user") || "null")

    if(to.meta.requiresAuth){

        if(!token){

            return "/login"

        }

        if(!user){
            return "/login"
        }

        if(to.meta.role && user.role != to.meta.role){

            return "/login"

        }

        if(
            user.role!="admin" && !user.profile_completed && !to.meta.allowIncomplete
        ){

            return "/complete-profile"

        }

    }

    return true

})

export default router
