<template>

    <DashboardLayout>

        <Loader v-if="loading" />

        <div v-else>

            <PageTitle :title="drive.title" />

            <div class="card">

                <div class="card-body">

                    <h5>{{ drive.company_name }}</h5>

                    <p>{{ drive.job_description }}</p>

                    <p><strong>Package:</strong> ₹ {{ drive.salary_package }} LPA</p>

                    <p><strong>Location:</strong> {{ drive.location }}</p>

                    <p><strong>Eligibility CGPA:</strong> {{ drive.eligibility_cgpa }}</p>

                    <p><strong>Graduation Year:</strong> {{ drive.eligibility_year }}</p>

                    <p><strong>Deadline:</strong> {{ drive.application_deadline }}</p>

                    <p><strong>Status:</strong>

                        <StatusBadge :status="drive.approval_status" />

                    </p>

                    <div class="mt-4">

                        <button v-if="drive.approval_status != 'approved'" class="btn btn-warning me-2"
                            @click="$router.push('/company/drives/' + drive.id + '/edit')">

                            Edit

                        </button>

                        <span v-else class="text-muted me-2">
                            Approved drives cannot be edited
                        </span>

                        <button class="btn btn-danger me-2" @click="showDeleteConfirm = true">

                            Delete

                        </button>

                        <button class="btn btn-primary" @click="viewApplicants">

                            Applicants

                        </button>

                    </div>

                </div>

            </div>

            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>

        </div>

        <ConfirmModal v-if="showDeleteConfirm" title="Delete Drive"
            message="Are you sure you want to delete this drive? This action cannot be undone." @confirm="confirmDelete"
            @cancel="showDeleteConfirm = false" />

    </DashboardLayout>

</template>

<script>

import api from "@/services/api"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import StatusBadge from "@/components/StatusBadge.vue"
import Loader from "@/components/Loader.vue"
import ConfirmModal from "@/components/ConfirmModal.vue"

export default {

    components: {
        DashboardLayout,
        PageTitle,
        StatusBadge,
        Loader,
        ConfirmModal
    },

    data() {

        return {

            drive: {},
            loading: true,
            error: "",
            showDeleteConfirm: false

        }

    },

    async mounted() {

        await this.loadDrive()

    },

    methods: {

        async loadDrive() {

            try {

                const response = await api.get(

                    "/company/drives/" + this.$route.params.id

                )

                this.drive = response.data

            }

            catch (error) {

                this.error = error.response?.data?.message || "Failed to load drive"

            }

            finally {

                this.loading = false

            }

        },

        async confirmDelete() {

            this.showDeleteConfirm = false

            try {

                await api.delete(

                    "/company/drives/" + this.drive.id

                )

                alert("Drive deleted successfully")

                this.$router.push("/company/drives")

            }

            catch (error) {

                this.error = error.response?.data?.message || "Failed to delete drive"

            }

        },

        viewApplicants() {

            this.$router.push(

                "/company/drives/" + this.drive.id + "/applicants"

            )

        }

    }

}

</script>
