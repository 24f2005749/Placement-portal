<template>

    <DashboardLayout>

        <PageTitle title="My Profile" />

        <StudentProfileForm />

    </DashboardLayout>

</template>

<script>

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import StudentProfileForm from "@/components/StudentProfileForm.vue"

export default {

    components: {
        DashboardLayout,
        PageTitle,
        StudentProfileForm
    }

}

</script>