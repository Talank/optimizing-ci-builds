##For getting unnecessary directories in top level
bash make_cluster_for_each_category.sh Output/JSQlParser-never-accessed "" Output/JSQlParser-useful  JSQLParser Clustering-Unused-Directories
bash make_cluster_for_each_category.sh Output/Algorithm-never-accessed "" Output/Algorithm-useful  Algorithm Clustering-Unused-Directories
bash make_cluster_for_each_category.sh Output/MavenTestCI-never-accessed ""  Output/MavenTestCI-useful  MavenTestCI Clustering-Unused-Directories
bash make_cluster_for_each_category.sh Output/jv-fruit-shop-never-accessed "" Output/jv-fruit-shop-useful  jv-fruit-shop Clustering-Unused-Directories
bash make_cluster_for_each_category.sh Output/matism-example-project-never-accessed  ""  Output/matism-example-project-useful  matism-example-project Clustering-Unused-Directories
bash make_cluster_for_each_category.sh Output/mcMMO-never-accessed ""  Output/mcMMO-useful  mcMMO Clustering-Unused-Directories
bash make_cluster_for_each_category.sh Output/pipelines-java-never-accessed ""  Output/pipelines-java-useful  pipelines-java Clustering-Unused-Directories
bash make_cluster_for_each_category.sh Output/spring-framework-petclinic-never-accessed "" Output/spring-framework-petclinic-useful spring-framework-petclinic Clustering-Unused-Directories
bash make_cluster_for_each_category.sh Output/spring-petclinic-rest-never-accessed "" Output/spring-petclinic-rest-useful spring-petclinic-rest Clustering-Unused-Directories

##For getting useful directories in top level
bash make_cluster_for_each_category.sh Output/JSQlParser-useful  "" Output/JSQlParser-never-accessed JSQLParser Clustering-Useful-Directories 
bash make_cluster_for_each_category.sh Output/Algorithm-useful  "" Output/Algorithm-never-accessed Algorithm Clustering-Useful-Directories
bash make_cluster_for_each_category.sh Output/MavenTestCI-useful  "" Output/MavenTestCI-never-accessed MavenTestCI Clustering-Useful-Directories
bash make_cluster_for_each_category.sh Output/jv-fruit-shop-useful  "" Output/jv-fruit-shop-never-accessed jv-fruit-shop Clustering-Useful-Directories
bash make_cluster_for_each_category.sh Output/matism-example-project-useful  "" Output/matism-example-project-never-accessed matism-example-project Clustering-Useful-Directories
bash make_cluster_for_each_category.sh Output/mcMMO-useful  "" Output/mcMMO-never-accessed mcMMO Clustering-Useful-Directories
bash make_cluster_for_each_category.sh Output/pipelines-java-useful  "" Output/pipelines-java-never-accessed pipelines-java Clustering-Useful-Directories
bash make_cluster_for_each_category.sh Output/spring-framework-petclinic-useful  "" Output/spring-framework-petclinic-never-accessed spring-framework-petclinic Clustering-Useful-Directories
bash make_cluster_for_each_category.sh Output/spring-petclinic-rest-useful  "" Output/spring-petclinic-rest-never-accessed spring-petclinic-rest Clustering-Useful-Directories