<template>
    <div class="bg-dark text-white min-vh-100">
        <h4 class="text-center py-4 fs-5">
            Menu
        </h4>
        <div class="list-group rounded-0">
            <router-link v-for="item in menu" :key="item.name" :to="item.route"
                class="list-group-item list-group-item-action" active-class="active">
                {{ item.name }}
            </router-link>
        </div>
    </div>
</template>

<script>
export default {
    props: ["role"],
    computed: {
        menu() {
            if (this.role == "student") {
                return [
                    { name: "Dashboard", route: "/student/dashboard" },
                    { name: "Drives", route: "/student/drives" },
                    { name: "Companies", route: "/student/companies" },
                    { name: "Applications", route: "/student/applications" },
                    { name: "Profile", route: "/student/profile" }
                ]
            }
            if (this.role == "company") {
                return [
                    { name: "Dashboard", route: "/company/dashboard" },
                    { name: "Drives", route: "/company/drives" },
                    { name: "Profile", route: "/company/profile" }
                ]
            }

            return [

                { name: "Dashboard", route: "/admin/dashboard" },
                { name: "Companies", route: "/admin/companies" },
                { name: "Drives", route: "/admin/drives" },
                { name: "Students", route: "/admin/students" },
                { name: "Applications", route: "/admin/applications" },
                { name: "Branches", route: "/admin/branches" }

            ]
        }
    }
}

</script>
