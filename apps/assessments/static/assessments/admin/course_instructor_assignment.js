document.addEventListener(
    "DOMContentLoaded",
    function () {

        const courseField =
            document.getElementById(
                "id_course"
            );

        const instructorField =
            document.getElementById(
                "id_instructor"
            );

        if (
            !courseField ||
            !instructorField
        ) {
            console.error(
                "Course or instructor field not found"
            );

            return;
        }


        console.log(
            "COURSE INSTRUCTOR JS LOADED"
        );


        function loadInstructors() {

            const courseId =
                courseField.value;

            console.log(
                "COURSE ID:",
                courseId
            );


            instructorField.innerHTML =
                "";


            const loadingOption =
                document.createElement(
                    "option"
                );

            loadingOption.value =
                "";

            loadingOption.textContent =
                "در حال بارگذاری...";


            instructorField.appendChild(
                loadingOption
            );


            if (!courseId) {

                loadingOption.textContent =
                    "ابتدا دوره را انتخاب کنید.";

                return;
            }


            const url =
                "../instructors-for-course/" +
                "?course_id=" +
                encodeURIComponent(
                    courseId
                );


            console.log(
                "REQUEST URL:",
                url
            );


            fetch(url)
                .then(
                    response => {

                        console.log(
                            "API STATUS:",
                            response.status
                        );


                        if (!response.ok) {

                            throw new Error(
                                "HTTP " +
                                response.status
                            );
                        }


                        return response.json();
                    }
                )
                .then(
                    data => {

                        console.log(
                            "API DATA:",
                            data
                        );


                        instructorField.innerHTML =
                            "";


                        const emptyOption =
                            document.createElement(
                                "option"
                            );

                        emptyOption.value =
                            "";

                        emptyOption.textContent =
                            "---------";


                        instructorField.appendChild(
                            emptyOption
                        );


                        data.instructors.forEach(
                            instructor => {

                                const option =
                                    document.createElement(
                                        "option"
                                    );

                                option.value =
                                    instructor.id;

                                option.textContent =
                                    instructor.name;


                                instructorField.appendChild(
                                    option
                                );
                            }
                        );
                    }
                )
                .catch(
                    error => {

                        console.error(
                            "INSTRUCTOR ERROR:",
                            error
                        );


                        instructorField.innerHTML =
                            "";


                        const errorOption =
                            document.createElement(
                                "option"
                            );

                        errorOption.value =
                            "";

                        errorOption.textContent =
                            "خطا در دریافت مدرس";


                        instructorField.appendChild(
                            errorOption
                        );
                    }
                );
        }


        /*
         * Native change
         */
        courseField.addEventListener(
            "change",
            function () {

                console.log(
                    "NATIVE CHANGE"
                );

                loadInstructors();
            }
        );


        /*
         * Django Select2
         */
        if (
            window.django &&
            window.django.jQuery
        ) {

            const $ =
                window.django.jQuery;


            $(courseField).on(
                "select2:select",
                function () {

                    console.log(
                        "SELECT2 SELECT"
                    );

                    loadInstructors();
                }
            );


            $(courseField).on(
                "change",
                function () {

                    console.log(
                        "JQUERY CHANGE"
                    );

                    loadInstructors();
                }
            );
        }

    }
);