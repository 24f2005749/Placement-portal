<template>
    <div class="app-shell">
        <Navbar/>
        <div class="container-fluid">
            <div class="row">
                <div class="col-lg-2 col-md-3 p-0 sidebar-column">
                    <Sidebar :role="user.role"/>
                </div>

                <div class="col-lg-10 col-md-9 p-4">
                    <slot></slot>
                </div>
                
            </div>
        </div>
    </div>
</template>

<script>

    import Navbar from "@/components/Navbar.vue"
    import Sidebar from "@/components/Sidebar.vue"

    export default{

        components:{
            Navbar,
            Sidebar
        },

        data(){
            return{
                user:JSON.parse(localStorage.getItem("user"))
            }
        }
    }

</script>
