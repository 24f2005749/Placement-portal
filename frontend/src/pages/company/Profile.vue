<template>

    <DashboardLayout>

        <PageTitle title="Company Profile" />

        <CompanyProfileForm />

    </DashboardLayout>

</template>

<script>

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import CompanyProfileForm from "@/components/CompanyProfileForm.vue"

export default {

    components: {
        DashboardLayout,
        PageTitle,
        CompanyProfileForm
    }

}

</script>