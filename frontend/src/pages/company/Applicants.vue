<template>

    <DashboardLayout>

        <PageTitle title="Applicants" />

        <Loader v-if="loading" />

        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

        <EmptyState v-else-if="applicants.length == 0" message="No applicants yet" />

        <DashboardTable v-else title="Student Applications">

            <template #head>

                <th>Name</th>
                <th>Roll #</th>
                <th>CGPA</th>
                <th>Resume</th>
                <th>Status</th>
                <th>Action</th>

            </template>

            <template #body>

                <tr v-for="student in applicants" :key="student.application_id">

                    <td>

                        {{ student.student_name }}

                    </td>

                    <td>

                        {{ student.roll_number }}

                    </td>

                    <td>

                        {{ student.cgpa }}

                    </td>

                    <td>

                        <a v-if="student.resume" :href="student.resume" target="_blank" rel="noopener noreferrer"
                            class="btn btn-outline-primary btn-sm">

                            View resume

                        </a>

                        <span v-else class="text-muted">Not provided</span>

                    </td>

                    <td>

                        <StatusBadge :status="student.status" />

                    </td>

                    <td>

                        <button class="btn btn-primary btn-sm" @click="manage(student)">

                            Manage

                        </button>

                    </td>

                </tr>

            </template>

        </DashboardTable>

        <ManageApplicationModal v-if="selected" :application="selected" @close="selected = null"
            @updated="fetchApplicants" />

    </DashboardLayout>

</template>

<script>

import api from "@/services/api"

import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DashboardTable from "@/components/DashboardTable.vue"
import PageTitle from "@/components/PageTitle.vue"
import StatusBadge from "@/components/StatusBadge.vue"
import ManageApplicationModal from "@/components/ManageApplicationModal.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"

export default {

    components: {
        DashboardLayout,
        DashboardTable,
        PageTitle,
        StatusBadge,
        ManageApplicationModal,
        Loader,
        EmptyState
    },

    data() {

        return {

            applicants: [],
            selected: null,
            loading: true,
            error: ""

        }

    },

    async mounted() {

        await this.fetchApplicants()

    },

    methods: {

        async fetchApplicants() {

            this.loading = true
            this.error = ""

            try {

                const response = await api.get(

                    "/company/drives/" + this.$route.params.id + "/applications"

                )

                this.applicants = response.data

            }

            catch (error) {

                this.error = error.response?.data?.message || "Failed to load applicants"

                console.error(error)

            }

            finally {

                this.loading = false

            }

        },

        manage(student) {

            this.selected = student

        }

    }

}

</script>
