<template>
    <DashboardLayout>
        <PageTitle title="Edit Drive" />
        <DriveForm mode="edit" :drive-id="$route.params.id" />
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
