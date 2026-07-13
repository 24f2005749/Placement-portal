<template>
    <DashboardLayout>
        <PageTitle title="Student Management" />

        <SearchBar @search="search" />

        <div class="row g-2 mt-3">
            <div class="col-md-8">
                <select v-model="selectedDriveId" class="form-select" @change="fetchStudents">
                    <option value="">All students</option>
                    <option v-for="drive in drives" :key="drive.id" :value="drive.id">
                        {{ drive.company_name }} - {{ drive.title }}
                    </option>
                </select>
            </div>
            <div class="col-md-4">
                <select v-model="eligibilityFilter" class="form-select" :disabled="!selectedDriveId" @change="fetchStudents">
                    <option value="">All eligibility</option>
                    <option value="true">Eligible</option>
                    <option value="false">Not eligible</option>
                </select>
            </div>
        </div>

        <Loader v-if="loading" class="mt-4" />
        <div v-else-if="error" class="alert alert-danger mt-4">{{ error }}</div>
        <EmptyState
            v-else-if="filteredStudents.length === 0"
            message="No students found."
        />

        <DashboardTable v-else-if="filteredStudents.length" title="Students">
            <template #head>
                <th>Name</th>
                <th>Roll #</th>
                <th>Branch</th>
                <th>CGPA</th>
                <th>Graduation Year</th>
                <th v-if="selectedDriveId">Eligibility</th>
                <th>Active</th>
                <th>Actions</th>
            </template>
            <template #body>
                <tr v-for="student in filteredStudents" :key="student.id">
                    <td>{{ student.full_name }}</td>
                    <td>{{ student.roll_number }}</td>
                    <td>{{ student.branch }}</td>
                    <td>{{ student.cgpa }}</td>
                    <td>{{ student.graduation_year }}</td>
                    <td v-if="selectedDriveId">
                        <span v-if="student.eligible_for_drive" class="badge text-bg-success">Eligible</span>
                        <span v-else class="badge text-bg-warning">{{ student.eligibility_message || "Not eligible" }}</span>
                    </td>
                    <td>{{ student.active ? "Yes" : "No" }}</td>
                    <td>
                        <button class="btn btn-sm" :class="student.active ? 'btn-outline-danger' : 'btn-outline-success'" @click="toggleStudent(student)">
                            {{ student.active ? "Deactivate" : "Activate" }}
                        </button>
                    </td>
                </tr>
            </template>
        </DashboardTable>
    </DashboardLayout>
</template>

<script>
import api from "@/services/api"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DashboardTable from "@/components/DashboardTable.vue"
import PageTitle from "@/components/PageTitle.vue"
import SearchBar from "@/components/SearchBar.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"
import { showToast } from "@/utils/toast"

export default {
    components: { DashboardLayout, DashboardTable, PageTitle, SearchBar, Loader, EmptyState },

    data() {
        return {
            students: [],
            drives: [],
            searchText: "",
            selectedDriveId: "",
            eligibilityFilter: "",
            loading: true,
            error: ""
        }
    },

    computed: {
        filteredStudents() {
            if(!this.searchText.trim()){
                return this.students
            }

            const search = this.searchText.toLowerCase()

            return this.students.filter(student =>
                student.full_name.toLowerCase().includes(search)
                || student.roll_number.toLowerCase().includes(search)
                || student.branch.toLowerCase().includes(search)
            )
        }
    },

    async mounted() {
        await this.fetchDrives()
        await this.fetchStudents()
    },

    methods: {
        async fetchDrives() {
            try {
                const response = await api.get("/admin/drives")
                this.drives = response.data
            } catch (error) {
                this.error = error.response?.data?.message || "Failed to load drives"
            }
        },

        async fetchStudents() {
            this.loading = true
            this.error = ""

            try {
                const params = {}

                if(this.selectedDriveId){
                    params.drive_id = this.selectedDriveId
                }

                if(this.selectedDriveId && this.eligibilityFilter){
                    params.eligible = this.eligibilityFilter
                }

                const response = await api.get("/admin/students",{ params })
                this.students = response.data
            } catch (error) {
                this.error = error.response?.data?.message || "Failed to load students"
            } finally {
                this.loading = false
            }
        },

        search(q) {
            this.searchText = q
        },

        async toggleStudent(student) {
            try {
                await api.put("/admin/students/"+student.id,{active:!student.active})
                showToast("Student updated successfully","success")
                await this.fetchStudents()
            } catch (error) {
                showToast(error.response?.data?.message || "Failed to update student","danger")
            }
        }
    }
}
</script>
