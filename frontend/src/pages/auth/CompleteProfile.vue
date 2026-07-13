<template>
    <DashboardLayout>
        <StudentProfileForm v-if="user.role == 'student'" />
        <CompanyProfileForm v-else />
    </DashboardLayout>
</template>
<script>
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import StudentProfileForm from "@/components/StudentProfileForm.vue"
import CompanyProfileForm from "@/components/CompanyProfileForm.vue"
export default {
    components: {
        DashboardLayout,
        StudentProfileForm,
        CompanyProfileForm
    },
    data() {
        return {
            user: JSON.parse(localStorage.getItem("user"))
        }
    }
}
</script>