<template>
    <DashboardLayout>
        <PageTitle title="Create Drive" />
        <DriveForm mode="create" />
    </DashboardLayout>
</template>

<script>
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import DriveForm from "@/components/DriveForm.vue"

export default {
    components: {
        DashboardLayout,
        PageTitle,
        DriveForm
    }
}
</script>
