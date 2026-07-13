<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow">
        <div class="container-fluid">
            <router-link class="navbar-brand fw-bold" to="/">
                Placement Portal
            </router-link>

            <div class="d-flex align-items-center">
                <span class="text-white me-3 d-none d-sm-inline">
                    {{ user.email }}
                </span>
                <span class="badge bg-light text-dark me-3">
                    {{ user.role }}
                </span>
                <button class="btn btn-outline-light" @click="showLogoutConfirm = true">
                    Logout
                </button>
            </div>
            
        </div>
    </nav>
    <ConfirmModal v-if="showLogoutConfirm" title="Log out?" message="Are you sure you want to log out?"
        confirm-text="Logout" cancel-text="Stay" @confirm="logout" @cancel="showLogoutConfirm = false" />
</template>

<script>

import ConfirmModal from "@/components/ConfirmModal.vue"

export default {
    components: {
        ConfirmModal
    },
    data() {
        return {
            user: JSON.parse(localStorage.getItem("user")) || {},
            showLogoutConfirm: false
        }
    },
    methods: {
        logout() {
            this.showLogoutConfirm = false
            localStorage.clear()
            this.$router.push("/login")
        }
    }
}

</script>
