

    $(document).ready(function () {

        $("#submitBtn, #nextQuestionBtn").prop("disabled", true);

        // Listen for changes in the radio buttons
        $("input[name='choice']").change(function () {
            // Check if at least one radio button is selected
            var isAnyRadioButtonSelected = $("input[name='choice']").is(":checked");

            // Enable or disable the submit button based on the selection status
            $("#submitBtn").prop("disabled", !isAnyRadioButtonSelected);
        });


        $("#submitBtn").click(function () {
            // Get the value of the selected radio button
            var selectedChoice = $("input[name='choice']:checked").val();
            var questionId = $('#questionId').val();
            console.log(questionId)
            // Do something with the selectedChoice

            var csrftoken = $("[name=csrfmiddlewaretoken]").val();

            $.ajax({
                method: 'POST',
                url: '{% url "quiz:check_answer" %}',  // Replace with your actual URL

                data: {
                    'selectChoice': selectedChoice,
                    'question_id': questionId,
                    csrfmiddlewaretoken: csrftoken  // Include CSRF token in data payload
                },

                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function (response) {
                    // Handle the response as needed
                    console.log(response)
                    if (response['is_correct'] === true) {
                        $("#descriptionParagraph").show();
                        $("#wrong-answer").hide();
                        $("#submission_button").hide();
                    } else {
                        $("#descriptionParagraph").show();
                        $("#correct-answer").hide();
                        $("#submission_button").hide();
                    }
                },
                error: function (error) {
                    console.log(error);
                    // Handle the error as needed
                }
            });

            // Show the description page
        });

    });






    // JavaScript to increase the progress bar value
    function increaseProgressBar() {
        var progressBar = document.getElementById("myProgressBar");
        var currentValue = parseInt(progressBar.style.width, 10) || 0;
        var newValue = currentValue + 10; // Increase by 10% (you can adjust this value)

        if (newValue <= 100) {
            progressBar.style.width = newValue + "%";
            progressBar.setAttribute("aria-valuenow", newValue);
        }
    }

    // Function to load the next question via AJAX
    function loadNextQuestion() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                // Update content on success
                document.body.innerHTML = xhr.responseText;
                increaseProgressBar(); // Call the progress bar function
            }
        };

        // Use Django URL template tag to get the correct URL
        var url = "{% url 'quiz:question_content' pk=next_question.pk %}";

        // Specify the URL to load
        xhr.open("GET", url, true);
        xhr.send();
    }






    <script>
    $(document).ready(function () {
        $("#submitBtn").prop("disabled", true);

        // Listen for changes in the radio buttons
        $("input[name='choice']").change(function () {
            // Check if at least one radio button is selected
            var isAnyRadioButtonSelected = $("input[name='choice']").is(":checked");

            // Enable or disable the submit button based on the selection status
            $("#submitBtn").prop("disabled", !isAnyRadioButtonSelected);
        });

        $("#submitBtn").click(function () {
            // Get the value of the selected radio button
            var selectedChoice = $("input[name='choice']:checked").val();
            var questionId = $('#questionId').val();

            var csrftoken = $("[name=csrfmiddlewaretoken]").val();

            $.ajax({
                method: 'POST',
                url: '{% url "quiz:check_answer" %}',  // Replace with your actual URL

                data: {
                    'selectChoice': selectedChoice,
                    'question_id': questionId,
                    csrfmiddlewaretoken: csrftoken  // Include CSRF token in data payload
                },

                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function (response) {
                    // Handle the response as needed
                    console.log(response);
                    if (response['is_correct'] === true) {
                        $("#descriptionParagraph").show();
                        $("#wrong-answer").hide();
                        $("#submission_button").hide();
                    } else {
                        $("#descriptionParagraph").show();
                        $("#correct-answer").hide();
                        $("#submission_button").hide();
                    }
                },
                error: function (error) {
                    console.log(error);
                    // Handle the error as needed
                }
            });

            // Show the description page
        });

        // Function to increase the progress bar
        function increaseProgressBar() {
            var progressBar = document.getElementById("myProgressBar");
            var currentValue = parseInt(progressBar.style.width, 10) || 0;
            var newValue = currentValue + 10; // Increase by 10% (you can adjust this value)

            if (newValue <= 100) {
                progressBar.style.width = newValue + "%";
                progressBar.setAttribute("aria-valuenow", newValue);
            }
        }

        // Function to load the next question via AJAX
        function loadNextQuestion() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    // Update content on success
                    document.body.innerHTML = xhr.responseText;
                    increaseProgressBar(); // Call the progress bar function
                }
            };

            // Use Django URL template tag to get the correct URL
            var url = "{% url 'quiz:question_content' pk=next_question.pk %}";

            // Specify the URL to load
            xhr.open("GET", url, true);
            xhr.send();
        }

        // Assign the loadNextQuestion function to the Next Question button
        $("#nextQuestionBtn").click(loadNextQuestion);
    });
















<script>
    $(document).ready(function () {
        $("#submitBtn").prop("disabled", true);

        function increaseProgressBar() {
            var progressBar = document.getElementById("myProgressBar");
            var currentValue = parseInt(progressBar.style.width, 10) || 0;
            var newValue = currentValue + 10; // Increase by 10% (you can adjust this value)

            if (newValue <= 100) {
                progressBar.style.width = newValue + "%";
                progressBar.setAttribute("aria-valuenow", newValue);
            }
        }

        // Listen for changes in the radio buttons
        $("input[name='choice']").change(function () {
            // Check if at least one radio button is selected
            var isAnyRadioButtonSelected = $("input[name='choice']").is(":checked");

            // Enable or disable the submit button based on the selection status
            $("#submitBtn").prop("disabled", !isAnyRadioButtonSelected);
        });

        $("#submitBtn").click(function () {
            // Get the value of the selected radio button
            increaseProgressBar(); // Call the progress bar function
            var selectedChoice = $("input[name='choice']:checked").val();
            var questionId = $('#questionId').val();

            var csrftoken = $("[name=csrfmiddlewaretoken]").val();

            $.ajax({
                method: 'POST',
                url: '{% url "quiz:check_answer" %}',  // Replace with your actual URL

                data: {
                    'selectChoice': selectedChoice,
                    'question_id': questionId,
                    csrfmiddlewaretoken: csrftoken  // Include CSRF token in data payload
                },

                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function (response) {
                    // Handle the response as needed
                    console.log(response);
                    if (response['is_correct'] === true) {
                        $("#descriptionParagraph").show();
                        $("#wrong-answer").hide();
                        $("#submission_button").hide();
                    } else {
                        $("#descriptionParagraph").show();
                        $("#correct-answer").hide();
                        $("#submission_button").hide();
                    }
                },
                error: function (error) {
                    console.log(error);
                    // Handle the error as needed
                }
            });

        });

    });
</script>